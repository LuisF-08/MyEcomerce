```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useCategoriaStore } from '@/stores/categoria'
import { useToast } from 'primevue/usetoast'

import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import Toast from 'primevue/toast'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import InputNumber from 'primevue/inputnumber'
import ToggleSwitch from 'primevue/toggleswitch'

import type { Categoria } from '@/types/categoria'

const store = useCategoriaStore()
const toast = useToast()

type CategoriaForm = {
  id?: number
  nome: string
  descricao: string
  imagem: File | string | null
  ativo: boolean
  ordem: number
}

const editing = ref<CategoriaForm>({
  nome: '',
  descricao: '',
  imagem: null,
  ativo: true,
  ordem: 0
})

const deletingId = ref<number | null>(null)

const saving = ref(false)

const arquivoImagem = ref<File | null>(null)
const previewImagem = ref<string | null>(null)

const modalVisible = ref(false)
const deleteModalVisible = ref(false)


function toastSuccess(mensagem: string) {
  toast.add({
    severity: 'success',
    summary: 'Sucesso',
    detail: mensagem,
    life: 3000
  })
}


function toastError(mensagem: string) {
  toast.add({
    severity: 'error',
    summary: 'Erro',
    detail: mensagem,
    life: 4000
  })
}


onMounted(() => {
  store.carregarCategorias()
})


function blankForm(): CategoriaForm {
  return {
    nome: '',
    descricao: '',
    imagem: null,
    ativo: true,
    ordem: store.categorias.length
  }
}


function abrirModalNovo() {
  editing.value = blankForm()

  arquivoImagem.value = null
  previewImagem.value = null

  modalVisible.value = true
}


function abrirModalEdicao(categoria: Categoria) {
  editing.value = {
    id: categoria.id,
    nome: categoria.nome,
    descricao: categoria.descricao,
    imagem: categoria.imagem,
    ativo: categoria.ativo,
    ordem: categoria.ordem
  }

  arquivoImagem.value = null

  previewImagem.value =
    typeof categoria.imagem === 'string'
      ? categoria.imagem
      : null

  modalVisible.value = true
}


function fecharModal() {
  modalVisible.value = false

  editing.value = blankForm()

  arquivoImagem.value = null
  previewImagem.value = null
}


function confirmarExclusao(id: number) {
  deletingId.value = id
  deleteModalVisible.value = true
}


function onFileChange(event: Event) {
  const target = event.target as HTMLInputElement

  if (!target.files || !target.files[0]) {
    return
  }

  const file = target.files[0]

  // Libera preview anterior
  if (previewImagem.value?.startsWith('blob:')) {
    URL.revokeObjectURL(previewImagem.value)
  }

  arquivoImagem.value = file

  previewImagem.value = URL.createObjectURL(file)
}


function removerImagemSelecionada() {
  if (previewImagem.value?.startsWith('blob:')) {
    URL.revokeObjectURL(previewImagem.value)
  }

  arquivoImagem.value = null
  previewImagem.value = null
  editing.value.imagem = null
}


function buildFormData(): FormData {
  const formData = new FormData()

  formData.append(
    'nome',
    editing.value.nome.trim()
  )

  formData.append(
    'descricao',
    editing.value.descricao?.trim() ?? ''
  )

  formData.append(
    'ativo',
    editing.value.ativo ? 'true' : 'false'
  )

  formData.append(
    'ordem',
    String(editing.value.ordem ?? 0)
  )

  if (arquivoImagem.value instanceof File) {
    formData.append(
      'imagem',
      arquivoImagem.value
    )
  } else if (editing.value.imagem === null && editing.value.id) {
    formData.append('imagem', '')
  }

  return formData
}


async function salvar() {
  if (!editing.value.nome.trim()) {
    toast.add({
      severity: 'warn',
      summary: 'Atenção',
      detail: 'Informe o nome da categoria.',
      life: 3000
    })

    return
  }

  saving.value = true

  try {
    const formData = buildFormData()

    if (editing.value.id) {
      await store.atualizar(
        editing.value.id,
        formData
      )

      toastSuccess('Categoria atualizada!')
    } else {
      await store.criar(formData)

      toastSuccess('Categoria criada!')
    }

    fecharModal()

  } catch (error: any) {

    console.error(
      'Erro ao salvar categoria:',
      error?.response?.data ?? error
    )

    const detalhes =
      error?.response?.data

    if (detalhes) {
      console.error(
        'Detalhes da API:',
        detalhes
      )
    }

    toastError(
      'Erro ao salvar categoria. Verifique os dados.'
    )

  } finally {
    saving.value = false
  }
}


async function toggleAtivo(categoria: Categoria) {
  try {

    const formData = new FormData()

    formData.append(
      'ativo',
      categoria.ativo ? 'false' : 'true'
    )

    await store.atualizar(
      categoria.id,
      formData
    )

    toastSuccess('Status atualizado!')

  } catch (error) {

    console.error(
      'Erro ao atualizar status:',
      error
    )

    toastError(
      'Erro ao atualizar status.'
    )
  }
}


async function doDelete() {
  if (deletingId.value == null) {
    return
  }

  try {

    await store.remover(
      deletingId.value
    )

    toastSuccess(
      'Categoria removida.'
    )

  } catch {

    toastError(
      'Erro ao remover categoria.'
    )

  } finally {

    deleteModalVisible.value = false
    deletingId.value = null
  }
}
</script>
```


<template>
  <div class="space-y-4">
    <Toast />

    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-lg font-bold text-zinc-900">Categorias</h2>
        <p class="text-sm text-zinc-500">{{ store.categorias.length }} categorias</p>
      </div>
      <Button
        label="Nova categoria"
        icon="pi pi-plus"
        class="!bg-orange-500 !border-orange-500 hover:!bg-orange-600 !rounded-xl !font-semibold"
        @click="abrirModalNovo"
      />
    </div>

    <p v-if="store.erro" class="text-sm text-red-500">{{ store.erro }}</p>

    <div v-if="store.carregando" class="text-sm text-zinc-500">
      Carregando categorias...
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      <div
        v-for="cat in store.categorias"
        :key="cat.id"
        class="bg-white border border-zinc-200 rounded-2xl p-5 flex items-center gap-4"
        :class="!cat.ativo && 'opacity-60'"
      >
        <img
          v-if="cat.imagem"
          :src="cat.imagem"
          :alt="cat.nome"
          class="w-10 h-10 rounded-lg object-cover"
        />
        <div v-else class="w-10 h-10 rounded-lg bg-zinc-100" />

        <div class="flex-1">
          <p class="font-semibold text-zinc-800">{{ cat.nome }}</p>
          <p class="text-xs text-zinc-500">{{ cat.descricao }}</p>
        </div>

        <div class="flex items-center gap-2">
          <ToggleSwitch :model-value="cat.ativo" @update:model-value="() => toggleAtivo(cat)" />
          <Button icon="pi pi-pencil" size="small" text rounded @click="abrirModalEdicao(cat)" />
          <Button icon="pi pi-trash" size="small" text rounded severity="danger" @click="confirmarExclusao(cat.id)" />
        </div>
      </div>
    </div>

    <!-- Modal de criação/edição -->
    <Dialog
      v-model:visible="modalVisible"
      :header="editing.id ? 'Editar categoria' : 'Nova categoria'"
      :modal="true"
      :closable="!saving"
      :style="{ width: '420px' }"
      @hide="fecharModal"
    >
      <div class="space-y-4 py-2">
        <div>
          <label class="text-xs font-semibold text-zinc-600 mb-1 block">Nome *</label>
          <InputText v-model="editing.nome" class="w-full" placeholder="Ex: Roupas" />
        </div>

        <div>
          <label class="text-xs font-semibold text-zinc-600 mb-1 block">Descrição</label>
          <Textarea v-model="editing.descricao" class="w-full" rows="3" placeholder="Descrição da categoria" />
        </div>

        <!-- Upload de imagem (arquivo, não URL) -->
        <div>
          <label class="text-xs font-semibold text-zinc-600 mb-1 block">Imagem</label>
          <div class="flex items-center gap-3">
            <img
              v-if="previewImagem"
              :src="previewImagem"
              class="w-12 h-12 rounded-lg object-cover border border-zinc-200"
              alt="Preview"
            />
            <div v-else class="w-12 h-12 rounded-lg bg-zinc-100 border border-zinc-200" />

            <div class="flex-1">
              <input
                type="file"
                accept="image/*"
                @change="onFileChange"
                class="block w-full text-xs text-zinc-500 file:mr-2 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-orange-50 file:text-orange-600 hover:file:bg-orange-100 cursor-pointer"
              />
              <button
                v-if="previewImagem"
                type="button"
                class="text-xs text-red-500 hover:underline mt-1"
                @click="removerImagemSelecionada"
              >
                Remover imagem
              </button>
            </div>
          </div>
        </div>

        <div>
          <label class="text-xs font-semibold text-zinc-600 mb-1 block">Ordem</label>
          <InputNumber v-model="editing.ordem" class="w-full" :min="0" showButtons />
        </div>

        <div class="flex items-center gap-2">
          <ToggleSwitch v-model="editing.ativo" />
          <label class="text-sm text-zinc-700">Categoria ativa</label>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-3">
          <Button label="Cancelar" text :disabled="saving" @click="fecharModal" class="!rounded-xl" />
          <Button
            label="Salvar"
            :loading="saving"
            @click="salvar"
            class="!bg-orange-500 !border-orange-500 !rounded-xl"
          />
        </div>
      </template>
    </Dialog>

    <!-- Modal de exclusão -->
    <Dialog
      v-model:visible="deleteModalVisible"
      header="Confirmar exclusão"
      :modal="true"
      :style="{ width: '360px' }"
    >
      <p class="text-sm text-zinc-600 py-2">
        Tem certeza que deseja remover esta categoria? Esta ação não pode ser desfeita.
      </p>
      <template #footer>
        <div class="flex justify-end gap-3">
          <Button label="Cancelar" text @click="deleteModalVisible = false" class="!rounded-xl" />
          <Button label="Remover" severity="danger" @click="doDelete" class="!rounded-xl" />
        </div>
      </template>
    </Dialog>
  </div>
</template>
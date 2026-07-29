<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useProdutosStore } from '@/stores/produto'
import { useCategoriaStore } from '@/stores/categoria'
import { useToast } from 'primevue/usetoast'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import Toast from 'primevue/toast'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Textarea from 'primevue/textarea'
import Select from 'primevue/select'
import Checkbox from 'primevue/checkbox'
import Tag from 'primevue/tag'
import type { Produto } from '@/types/produto'

const store = useProdutosStore()
const catStore = useCategoriaStore()
const toast = useToast()

type ProdutoForm = Partial<Omit<Produto, 'id' | 'categoria_nome' | 'imagem_1' | 'imagem_2'>> & {
  id?: number
  imagem_1?: File | string | null
  imagem_2?: File | string | null
}

const editing = ref<ProdutoForm>({})
const deletingId = ref<number | null>(null)
const saving = ref(false)

// Refs para guardar os arquivos selecionados
const arquivoImagem1 = ref<File | null>(null)
const arquivoImagem2 = ref<File | null>(null)

const modalVisible = ref(false)
const deleteModalVisible = ref(false)

function toastSuccess(mensagem: string) {
  toast.add({ severity: 'success', summary: 'Sucesso', detail: mensagem, life: 3000 })
}

function toastError(mensagem: string) {
  toast.add({ severity: 'error', summary: 'Erro', detail: mensagem, life: 4000 })
}

onMounted(async () => {
  await Promise.allSettled([store.carregarProdutos(), catStore.carregarCategorias()])
})

function blankForm(): ProdutoForm {
  return {
    nome: '',
    preco: 0,
    descricao: '',
    categoria: undefined,
    quantidade: 0,
    destaque: false,
    ativo: true
  }
}

function openNew() {
  editing.value = blankForm()
  arquivoImagem1.value = null
  arquivoImagem2.value = null
  modalVisible.value = true
}

function openEdit(p: Produto) {
  const { categoria_nome: _categoria_nome, ...rest } = p
  editing.value = { ...rest }
  arquivoImagem1.value = null
  arquivoImagem2.value = null
  modalVisible.value = true
}

function confirmDelete(id: number) {
  deletingId.value = id
  deleteModalVisible.value = true
}

// Captura do arquivo no input HTML
function onFileChange(event: Event, field: 'imagem_1' | 'imagem_2') {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    if (field === 'imagem_1') arquivoImagem1.value = target.files[0]
    if (field === 'imagem_2') arquivoImagem2.value = target.files[0]
  }
}

// Monta o FormData necessário para upload de arquivos no Django
function buildFormData() {
    const formData = new FormData()
  
    if (editing.value.nome) formData.append('nome', editing.value.nome)
    if (editing.value.descricao) formData.append('descricao', editing.value.descricao)
    
    formData.append('preco', String(editing.value.preco ?? 0))
    formData.append('quantidade', String(editing.value.quantidade ?? 0))
    
    // O Django REST espera 'true' ou 'false' como string no FormData
    formData.append('ativo', editing.value.ativo ? 'true' : 'false')
    formData.append('destaque', editing.value.destaque ? 'true' : 'false')
    
    if (editing.value.categoria) {
        formData.append('categoria', String(editing.value.categoria))
    }
    
    // Anexa somente se o arquivo foi realmente selecionado pelo usuário
    if (arquivoImagem1.value instanceof File) {
        formData.append('imagem_1', arquivoImagem1.value)
    }
    
    if (arquivoImagem2.value instanceof File) {
        formData.append('imagem_2', arquivoImagem2.value)
    }

    return formData
}

async function save() {
  saving.value = true
  try {
    const payload = buildFormData()
    if (editing.value.id) {
      await store.atualizar(editing.value.id, payload as any)
      toastSuccess('Produto atualizado!')
    } else {
      await store.criar(payload as any)
      toastSuccess('Produto criado!')
    }
    modalVisible.value = false
  } catch (err: any) {
    console.error('Erro retornado do Django:', err.response?.data)
    toastError('Erro ao salvar produto.')
  } finally {
    saving.value = false
  }
}

async function doDelete() {
  if (deletingId.value == null) return
  try {
    await store.remover(deletingId.value)
    toastSuccess('Produto removido.')
  } catch {
    toastError('Erro ao remover produto.')
  } finally {
    deleteModalVisible.value = false
    deletingId.value = null
  }
}

const preco = (v: number | string | null | undefined) => {
  if (v === null || v === undefined) return 'R$ 0,00'
  const valNum = Number(v)
  if (isNaN(valNum)) return 'R$ 0,00'
  return `R$ ${valNum.toFixed(2).replace('.', ',')}`
}

const categoriaOptions = computed(() => catStore.categorias)
</script>

<template>
  <div class="space-y-4">
    <Toast />

    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-lg font-bold text-zinc-900">Produtos</h2>
        <p class="text-sm text-zinc-500">{{ store.produtos.length }} produtos cadastrados</p>
      </div>
      <Button label="Novo produto" icon="pi pi-plus" @click="openNew"
        class="!bg-orange-500 !border-orange-500 hover:!bg-orange-600 !rounded-xl !font-semibold" />
    </div>

    <p v-if="store.erro" class="text-sm text-red-500">{{ store.erro }}</p>

    <div class="bg-white border border-zinc-200 rounded-2xl overflow-hidden">
      <DataTable :value="store.produtos" :loading="store.carregando" class="!text-sm">
        <Column field="imagem_1" header="Foto" style="width: 70px">
          <template #body="{ data }">
            <img
              v-if="data.imagem_1"
              :src="data.imagem_1"
              class="w-10 h-10 object-cover rounded-lg"
              :alt="data.nome"
            />
            <div v-else class="w-10 h-10 rounded-lg bg-zinc-100" />
          </template>
        </Column>
        <Column field="nome" header="Nome" sortable />
        <Column field="categoria_nome" header="Categoria" sortable />
        <Column field="preco" header="Preço" sortable>
          <template #body="{ data }">{{ preco(data.preco) }}</template>
        </Column>
        <Column field="quantidade" header="Estoque" sortable />
        <Column field="destaque" header="Destaque">
          <template #body="{ data }">
            <Tag :value="data.destaque ? 'Sim' : 'Não'" :severity="data.destaque ? 'success' : 'secondary'" />
          </template>
        </Column>
        <Column field="ativo" header="Ativo">
          <template #body="{ data }">
            <Tag :value="data.ativo ? 'Ativo' : 'Inativo'" :severity="data.ativo ? 'success' : 'danger'" />
          </template>
        </Column>
        <Column header="Ações" style="width: 120px">
          <template #body="{ data }">
            <div class="flex gap-2">
              <Button icon="pi pi-pencil" size="small" text rounded @click="openEdit(data)" />
              <Button icon="pi pi-trash" size="small" text rounded severity="danger" @click="confirmDelete(data.id)" />
            </div>
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- Edit/New Dialog -->
    <Dialog
      v-model:visible="modalVisible"
      :header="editing.id ? 'Editar produto' : 'Novo produto'"
      :modal="true"
      :style="{ width: '560px' }"
    >
      <div class="space-y-4 py-2">
        <div>
          <label class="text-xs font-semibold text-zinc-600 mb-1 block">Nome *</label>
          <InputText v-model="editing.nome" class="w-full" placeholder="Nome do produto" />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="text-xs font-semibold text-zinc-600 mb-1 block">Preço *</label>
            <InputNumber v-model="editing.preco" mode="currency" currency="BRL" locale="pt-BR" class="w-full" />
          </div>
          <div>
            <label class="text-xs font-semibold text-zinc-600 mb-1 block">Quantidade</label>
            <InputNumber v-model="editing.quantidade" class="w-full" :min="0" />
          </div>
        </div>

        <div>
          <label class="text-xs font-semibold text-zinc-600 mb-1 block">Categoria</label>
          <Select
            v-model="editing.categoria"
            :options="categoriaOptions"
            option-label="nome"
            option-value="id"
            placeholder="Selecionar"
            class="w-full !rounded-xl"
          />
        </div>

        <!-- Inputs do tipo FILE para Upload de Imagens -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="text-xs font-semibold text-zinc-600 mb-1 block">Foto Principal</label>
            <input
              type="file"
              accept="image/*"
              @change="(e) => onFileChange(e, 'imagem_1')"
              class="block w-full text-xs text-zinc-500 file:mr-2 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-orange-50 file:text-orange-600 hover:file:bg-orange-100 cursor-pointer"
            />
          </div>
          <div>
            <label class="text-xs font-semibold text-zinc-600 mb-1 block">Foto Secundária</label>
            <input
              type="file"
              accept="image/*"
              @change="(e) => onFileChange(e, 'imagem_2')"
              class="block w-full text-xs text-zinc-500 file:mr-2 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-orange-50 file:text-orange-600 hover:file:bg-orange-100 cursor-pointer"
            />
          </div>
        </div>

        <div>
          <label class="text-xs font-semibold text-zinc-600 mb-1 block">Descrição</label>
          <Textarea v-model="editing.descricao" rows="3" class="w-full" />
        </div>

        <div class="flex items-center gap-6">
          <div class="flex items-center gap-2">
            <Checkbox v-model="editing.destaque" :binary="true" inputId="destaque" />
            <label for="destaque" class="text-sm text-zinc-700">Produto em destaque</label>
          </div>
          <div class="flex items-center gap-2">
            <Checkbox v-model="editing.ativo" :binary="true" inputId="ativo" />
            <label for="ativo" class="text-sm text-zinc-700">Produto ativo</label>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-3">
          <Button label="Cancelar" text @click="modalVisible = false" class="!rounded-xl" />
          <Button label="Salvar" :loading="saving" @click="save" class="!bg-orange-500 !border-orange-500 !rounded-xl" />
        </div>
      </template>
    </Dialog>

    <!-- Delete Dialog -->
    <Dialog
      v-model:visible="deleteModalVisible"
      header="Confirmar exclusão"
      :modal="true"
      :style="{ width: '360px' }"
    >
      <p class="text-sm text-zinc-600 py-2">Tem certeza que deseja remover este produto? Esta ação não pode ser desfeita.</p>
      <template #footer>
        <div class="flex justify-end gap-3">
          <Button label="Cancelar" text @click="deleteModalVisible = false" class="!rounded-xl" />
          <Button label="Remover" severity="danger" @click="doDelete" class="!rounded-xl" />
        </div>
      </template>
    </Dialog>
  </div>
</template>
export interface Loja {
    id: number;
    nome: string;
    descricao: string;
    logo: string | null;
    banner_1: string | null;
    banner_2: string | null;
    banner_3: string | null;
    banner_4: string | null;

    telefone: string;
    whatsapp: string;
    email: string;
    instagram: string | null;
    facebook: string | null;
    pix: string;

    cpf: string;
    cnpj: string | null;
    cep: string;
    rua: string;
    numero: string;
    referencia: string | null;
    bairro: string;
    cidade: string;
    estado: string;

    cor_primaria: string;
    cor_secundaria: string;

    mensagem_whatsapp: string;
    horario_funcionamento: string;     // ex: "08:00"
    horario_fechamento: string;        // ex: "18:00"
    dias_funcionamento: 'S' | 'SS';

    ativo: boolean;
    criado_em: string;
    atualizado_em: string;
    slug: string;
}
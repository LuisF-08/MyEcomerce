import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth"; 

const routes = [
    {
        path: "/",
        name: "home", 
        component: () => import("../pages/client/Home.vue")
    },
    {
        path: '/produtos',
        name: 'produtos',
        component: () => import('@/pages/client/Produtos.vue')
    },
    {
        path: '/produto/:id',
        name: 'produto',
        component: () => import('@/pages/client/Produto.vue')
    },
    {
        path: '/categoria/:slug',
        name: 'categoria',
        component: () => import('@/pages/client/Produtos.vue')
    },
    {
        path: "/sobre",
        name: "sobre",
        component: () => import("../pages/client/Sobre.vue"),
    },
    
    {
        path: "/admin/login",
        name: "login", 
        component: () => import("../pages/admin/LoginAdmin.vue")
    },

    {
        path: "/admin",
        name: "admin-dashboard",
        component: () => import("../pages/admin/DashboardAdmin.vue"),
        meta: {
            requiresAuth: true
        }
    },
    
    {
        path: '/admin/categorias',
        name: 'admin-categorias',
        component: () => import("../pages/admin/CategoriaAdmin.vue"),
        meta: {
            requiresAuth: true
        }
    },

    {
        path: '/admin/produtos',
        name: 'admin-produtos',
        component: () => import('@/pages/admin/ProdutosAdmin.vue'),
        meta: {
            requiresAuth: true
        }
    },

    {
        path: '/admin/loja',
        name: 'admin-loja',
        component: () => import("../pages/admin/LojaAdmin.vue"),
        meta: {
            requiresAuth: true
        }
    },

    {
        path: '/admin/configuracoes',
        name: 'admin-config',
        component: () => import("../pages/admin/ConfiguracaoAdmin.vue"),
        meta: {
            requiresAuth: true
        }
    },

    {
        path: '/admin/solicitacoes',
        name: 'admin-solicitacoes',
        component: () => import('@/pages/admin/SolicitacoesAdmin.vue'),
        meta: {
            requiresAuth: true
        }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

// Guard de navegação para proteger as rotas
router.beforeEach((to) => {
    const auth = useAuthStore();

    // Se a rota exige autenticação e o usuário não está logado
    if (to.meta.requiresAuth && !auth.isAuthenticated) {
        return {
            name: "login" // Redireciona para a rota nomeada 'login'
        };
    }
});

// Exportando o router configurado
export default router;
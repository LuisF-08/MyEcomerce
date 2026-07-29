import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const routes = [
    {
        path: "/",
        component: () => import("@/components/layout/ClienteLayout.vue"),
        children: [
            {
                path: "",
                name: "home",
                component: () => import("@/pages/client/Home.vue")
            },
            {
                path: "produtos",
                name: "produtos",
                component: () => import("@/pages/client/Produtos.vue")
            },
            {
                path: "categoria/:slug",
                name: "categoria",
                component: () => import("@/pages/client/Produtos.vue")
            },
            {
                path: "produto/:id",
                name: "produto",
                component: () => import("@/pages/client/Produto.vue")
            },
            {
                path: "sobre",
                name: "sobre",
                component: () => import("@/pages/client/Sobre.vue")
            }
        ]
    },
    {
        path: "/login",
        name: "login",
        component: () => import("@/pages/admin/LoginAdmin.vue")
    },
    {
        path: "/admin",
        component: () => import("@/components/layout/AdminLayout.vue"),
        children: [
            {
                path: "",
                name: "admin-dashboard",
                component: () => import("@/pages/admin/DashboardAdmin.vue"),
                meta: {
                    requiresAuth: true
                }
            },
            {
                path: "produtos",
                name: "admin-produtos",
                component: () => import("@/pages/admin/ProdutosAdmin.vue"),
                meta: {
                    requiresAuth: true
                }
            },
            // 💡 ROTAS NOVAS usadas pela AppSidebar:
            {
                path: "categorias",
                name: "admin-categorias",
                component: () => import("@/pages/admin/CategoriaAdmin.vue"),
                meta: {
                    requiresAuth: true
                }
            },
            {
                path: "solicitacoes",
                name: "admin-solicitacoes",
                component: () => import("@/pages/admin/SolicitacoesAdmin.vue"),
                meta: {
                    requiresAuth: true
                }
            },
            {
                path: "loja",
                name: "admin-loja",
                component: () => import("@/pages/admin/LojaAdmin.vue"),
                meta: {
                    requiresAuth: true
                }
            },
            {
                path: "configuracoes",
                name: "admin-configuracoes",
                component: () => import("@/pages/admin/ConfiguracaoAdmin.vue"),
                meta: {
                    requiresAuth: true
                }
            }
        ]
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
        return savedPosition
    }
    if (to.hash) {
        return { el: to.hash, behavior: 'smooth' }
    }
    return { top: 0, behavior: 'instant' }
    },
})

// Guard de navegação para proteger as rotas
router.beforeEach((to) => {
    const auth = useAuthStore();
    if (to.meta.requiresAuth && !auth.autenticado) {
        return {
            name: "login"
        };
    }
});



export default router;
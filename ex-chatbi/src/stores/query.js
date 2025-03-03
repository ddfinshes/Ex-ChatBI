import { defineStore } from 'pinia';

export const useQueryStore = defineStore('query', {
    state: () => ({
        currentQuery: '', // 初始值为空字符串
        response: null
    }),
    actions: {
        setCurrentQuery(query) {
            this.currentQuery = query; // 更新 currentQuery 的方法
        },
        setResponse(response) {
            this.response = response; // 更新响应数据
        }
    }
});
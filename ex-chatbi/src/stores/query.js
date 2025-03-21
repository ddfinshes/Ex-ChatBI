import { defineStore } from 'pinia';
import axios from 'axios';

export const useQueryStore = defineStore('query', {
    state: () => ({
        currentQuery: '', // 初始值为空字符串
        response: null,
        sqlcode: "",
        isReady: false,
        isDataReady: false,
        subsqljson: '', // 点击table后的子sql信息
        sqlresponse: null
    }),
    actions: {
        setCurrentQuery(query) {
            this.currentQuery = query; // 更新 currentQuery 的方法
        },
        setResponse(response) {
            this.response = response; // 更新响应数据
        },
        async setCurrentSQL(code) {
            this.sqlcode = code;
            this.isReady = true;
        },
        setIsDataReady(value) {
            this.isDataReady = value;
        },
        setSubSQLJson(value) {
            this.subsqljson = value;
        },
        // 新增：从后端获取 response
        async fetchSQLResponse(sql) {
            try {
                console.log(sql)
                const res = await axios.post(
                    "/api/sql2json",
                    { data: sql },
                    { headers: { "Content-Type": "application/json" } }
                );
                this.sqlresponse = { code: sql, result: res.data }; // 更新 response
                this.isDataReady = true;
                console.log("Fetched response:", this.sqlresponse);
            } catch (error) {
                console.error("Error fetching SQL response:", error);
            }
        }
        // async fetchSQLResponse(sql) {
        //     const res = await axios.post(
        //     "/api/sql2json",
        //     { data: sql },
        //     { headers: { "Content-Type": "application/json" } }
        //     );
        //     return res.data;
        // }
    }
});
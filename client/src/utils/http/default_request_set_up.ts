import { useNotificationStore } from "../hooks/use_notification_store"
import type { DefaultServerRes } from "./default_server_res"

type postParams<T> = {
    url: string,
    contentType?: string
    data: T,
    token?: string
}

type getParams = {
    url: string,
    contentType?: string
    token?: string
}


type deleteParams<T> = {
    url: string;
    data?: T;
    contentType?: string;
    token?: string;
};


export class DefaultRequestSetUp {



    static headerType({ contentType, token }: { contentType: string, token?: string }) {
        const headers: Record<string, string> = { "Content-Type": contentType };
        if (token) headers["Authorization"] = `Bearer ${token}`;
        return headers;
    }


    static async post<TModel, TRes>({ url, contentType = "application/json", data, token }: postParams<TModel>): Promise<DefaultServerRes<TRes>> {
        const { showNotification } = useNotificationStore.getState()
        try {
            var res = await fetch(url, {
                method: 'POST',
                credentials: "include",
                headers: DefaultRequestSetUp.headerType({
                    contentType: contentType, token: token
                }),
                body: JSON.stringify(data)
            })
            const resData = await res.json() as TRes;

            if (res.status === 500) {
                showNotification("erro making this request", "error")
                console.error(res.text)
            }
            return {
                ...(resData as object),
                statusCode: (resData as any).status_code ?? res.status,

            } as DefaultServerRes<TRes>;
        } catch (e) {
            showNotification("error communicating with server... call technical team", "error")
            throw (e)
        }
    }



    static async get<TRes>({ url, contentType = "application/json", token }: getParams): Promise<DefaultServerRes<TRes>> {
        const { showNotification } = useNotificationStore.getState()
        try {
            var res = await fetch(url, {
                method: 'GET',
                credentials: "include",
                headers: DefaultRequestSetUp.headerType({
                    contentType: contentType, token: token
                }),
            })
            const resData = await res.json() as TRes;

            if (res.status === 500) {
                showNotification("erro making this request", "error")
                console.error(res.text)
            }
            return {
                ...(resData as object),
                statusCode: (resData as any).status_code ?? res.status,

            } as DefaultServerRes<TRes>;
        } catch (e) {
            showNotification("error communicating with server... call technical team", "error")
            throw (e)
        }
    }

    static async delete<TModel, TRes>({
        url,
        data,
        contentType = "application/json",
        token,
    }: deleteParams<TModel>): Promise<DefaultServerRes<TRes>> {
        const { showNotification } = useNotificationStore.getState();
        try {
            const res = await fetch(url, {
                method: "DELETE",
                credentials: "include",
                headers: DefaultRequestSetUp.headerType({ contentType, token }),
                body: data ? JSON.stringify(data) : undefined,
            });

            const resData = (await res.json()) as TRes;

            if (res.status === 500) {
                showNotification("Error performing delete request", "error");
                console.error(await res.text());
            }

            return {
                ...(resData as object),
                statusCode: (resData as any).status_code ?? res.status,
            } as DefaultServerRes<TRes>;
        } catch (e) {
            showNotification("Error communicating with server... call technical team", "error");
            throw e;
        }
    }

}
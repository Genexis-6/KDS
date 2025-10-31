import { create } from "zustand";
import { DefaultRequestSetUp } from "../http/default_request_set_up";
import type { loginResInterface } from "../../features/auth/view/component/handle_form_submission";
import { AllServerUrls } from "../http/all_server_url";



type useAuthTokenParam = {
    token?: string | null,
    setToken: (newToken: string) => void,
    getAcessToken: () => Promise<void>
}


export const useAuthTokenStore = create<useAuthTokenParam>(
    (set, get) => ({
        token: null,
        setToken: (newToken) => {
            set({ token: newToken })
        },
        getAcessToken: async () => {
            if (get().token !== null) return;
            var newToken = await getNewToken()
            set({ token: newToken });
        }
    })
)





async function getNewToken() {
    var res = await DefaultRequestSetUp.get<loginResInterface>({ url: AllServerUrls.getRefreshToken })
    // console.log(res.data.accessToken);
    return res.data.accessToken;
}
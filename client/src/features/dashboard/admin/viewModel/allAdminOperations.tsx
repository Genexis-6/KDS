import type { UseFormSetError } from "react-hook-form"
import { AddNewClassModel } from "../model/add_class_model"
import type { ClassFormValues } from "../view/components/AddNewClassForm"
import { DefaultRequestSetUp } from "../../../../utils/http/default_request_set_up"
import { useAllClassStore } from "../../../../utils/hooks/use_all_class"
import { AllServerUrls } from "../../../../utils/http/all_server_url"
import { useAuthTokenStore } from "../../../../utils/hooks/use_auth_token_store"
import { useNotificationStore } from "../../../../utils/hooks/use_notification_store"
import { useClassCreationStore } from "../../../../utils/hooks/use_class_creation_store"

type addClassType<T extends ClassFormValues> = {
    data: T
    setError: UseFormSetError<T>
}

export class AllAdminOperation {
    static async submitNewClassData({
        data,
        setError,
    }: addClassType<ClassFormValues>) {
        const fullTeacherName = `${data.title} ${data.teacherName}`.trim();
        const { token, getAcessToken } = useAuthTokenStore.getState()
        if (!token) await getAcessToken()

        const finalData = new AddNewClassModel({ className: data.className, teacherName: fullTeacherName })
        const res = await DefaultRequestSetUp.post<AddNewClassModel, void>({ url: AllServerUrls.addNewClass, data: finalData, token: token! })

        if (res.statusCode === 400) {
            setError("className", {
                message: res.message
            })

        } else {
            if (res.statusCode === 200) {
                await useAllClassStore.getState().getLatestUpdate()
                useNotificationStore.getState().showNotification(res.message, "success")
                useClassCreationStore.getState().setProgress(false)

            }
        }
    }

    static async deleteThisClass({ className }: { className: string }) {
        const { token, getAcessToken } = useAuthTokenStore.getState()
        if (!token) await getAcessToken()
        const res = await DefaultRequestSetUp.delete<void, void>({ url: `${AllServerUrls.deleteClass}?className=${className}`, token: token! })


        if (res.statusCode === 200) {
            await useAllClassStore.getState().getLatestUpdate()
        }
        useNotificationStore.getState().showNotification(res.message, res.statusCode === 400 ? "error" : "success")



    }
}

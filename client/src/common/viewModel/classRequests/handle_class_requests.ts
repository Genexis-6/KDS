import { AllServerUrls } from "../../../utils/http/all_server_url";
import { DefaultRequestSetUp } from "../../../utils/http/default_request_set_up";
import type { ClassModel } from "../../model/classModels/class_model";



export class HandleClassRequests{
    
    static async getAllClass() {
        const res = await DefaultRequestSetUp.get<ClassModel[]>({url:AllServerUrls.getAllClassUlr})
        
        return res.data
    }
}
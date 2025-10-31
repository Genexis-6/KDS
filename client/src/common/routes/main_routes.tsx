
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { NavigationSync } from "../component/navigation_sync";
import { AppUrl } from "./app_urls";
import Login from "../../features/auth/view/pages/Login";

export default function MainRoute() {
    return <>

        <BrowserRouter>
            <NavigationSync />
            <Routes >
                <Route path={AppUrl.login} element={<Login />}/>
            </Routes>
        </BrowserRouter>
    </>
}
import "../styles/admin_style.css";
import AddNewClassComponent from "../components/AddNewClassComponent";
import AddNewClassForm from "../components/AddNewClassForm";
import { useEffect } from "react";
import { useClassCreationStore } from "../../../../../utils/hooks/use_class_creation_store";
import { useAllClassStore } from "../../../../../utils/hooks/use_all_class";
import { usePopupStore } from "../../../../../utils/hooks/use_pop_up_menu";
import AllAvailableClass from "../components/AllAvailbleClassBody";


export default function AdminDashBoard() {
  const { inProgress, setProgress } = useClassCreationStore();
  const { allClass, getLatestUpdate } = useAllClassStore()
  const { openPopup, closePopup } = usePopupStore()

  useEffect(() => {
    setProgress(false);
    getLatestUpdate().then()

  }, []);

  return (
    <div className="container">
      <div className="row">
        <div className="col-12 mt-5">
          <div className={`admin-container ${inProgress || allClass.length === 0 && "align-items-center justify-content-center"}`} >
            {inProgress ? (
              <AddNewClassForm />
            ) : allClass.length === 0 ? (
              <AddNewClassComponent />
            ) : (
              <AllAvailableClass
                allClass={allClass}
                openPopup={openPopup}
                closePopup={closePopup}
              />
            )}
          </div>

        </div>
      </div>
    </div>
  );
}


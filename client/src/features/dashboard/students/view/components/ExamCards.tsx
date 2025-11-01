import examIcon from "../../../../../assets/images/exams.svg"

type examCardProps = {
    title: string,
    author: string,
    subjectId: string, 
    active: boolean, 

}

export default function ExamCard({
    title, author, subjectId, active = true
}:examCardProps) {
    return <div className="exam-card" onClick={()=>{console.log(subjectId)}}>
        <div className="image-container">
            <img src={examIcon} alt="" />
        </div>
        <div className="description">
            <h3>
                {title}
            </h3>
            <small>
                {author}
            </small>
        </div>
    </div>
}
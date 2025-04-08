import QuestionForm from "./question_form.jsx";

export default function Create() {
  const createQuestion = ({}) => {
    console.log("hi");
  }
  
  return (
    <div>
      <QuestionForm creation={false} handleSubmit={createQuestion} />
    </div>
  );
}
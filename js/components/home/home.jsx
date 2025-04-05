import Header from "./header.jsx";
import QuestionList from "./question_list.jsx";

export default function Home() {
  return (
    <div>
      <Header />
      {/* TODO filter & paginate pages, i.e. p1, 2, 3 */}
      <QuestionList />
    </div>
  );
}
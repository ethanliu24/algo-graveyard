import { useEffect, useState } from "react";
import { getReqHeader } from "../../utils/utils.js";
import QuestionList from "./question_list.jsx";
import PaginationBoxes from "./pagination_boxes.jsx";

export default function QuestionPanel() {
  const [questions, setQuestions] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(async () => {
    const data = await getQuestions();
    setQuestions(data.data);
    setPage(data.page);
    setTotalPages(data.pages);
  }, []);

  const getQuestions = async (queries) => {
    const req = {
      method: "GET",
      header: getReqHeader(),
    }

    return await fetch(`/api/questions?${queries ? queries : ""}`, req)
      .then(res => res.json())
      .then(json => json.data)
      .catch(err => {
        throw err;
      })
  };

  const fetchForPage = (page) => {

  };

  return (
    <div>
      {/* TODO filter & paginate pages, i.e. p1, 2, 3 */}
      <QuestionList questions={questions} />
      <PaginationBoxes page={page} totalPages={totalPages} fetchForPage={fetchForPage} />
    </div>
  );
}
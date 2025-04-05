import { useEffect, useState } from "react";
import { getReqHeader } from "../../utils/utils.js";
import QuestionList from "./question_list.jsx";
import PaginationBoxes from "./pagination_boxes.jsx";

export default function QuestionPanel() {
  const [questions, setQuestions] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(async () => {
    await fetchForPage(1);
  }, []);

  const fetchForPage = async (page, pageSize = null) => {
    let query = { page: page };
    query = pageSize !== null ? { per_page: pageSize, ...query } : query;
    const data = await getQuestions(query);
    setQuestions(data.data);
    setPage(data.page);
    setTotalPages(data.pages);
  };

  const getQuestions = async (queries = {}) => {
    const req = {
      method: "GET",
      header: getReqHeader(),
    }

    return await fetch(`/api/questions?${formatQueries(queries)}`, req)
      .then(res => res.json())
      .then(json => json.data)
      .catch(err => {
        throw err;
      })
  };

  const formatQueries = (queries) => {
    let queryStr = new URLSearchParams(queries).toString();
    return queryStr;
  };

  return (
    <div className="mt-4">
      {/* TODO filter & paginate pages, i.e. p1, 2, 3 */}
      <QuestionList questions={questions} />
      <PaginationBoxes page={page} totalPages={totalPages} fetchForPage={fetchForPage} />
    </div>
  );
}
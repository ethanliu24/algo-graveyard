import { useEffect, useState } from "react";
import { getReqHeader, formatQueries } from "../../utils/utils.js";
import QuestionList from "./question_list.jsx";
import PaginationBoxes from "./pagination_boxes.jsx";
import FilterBar from "./filter_bar.jsx";

export default function QuestionPanel() {
  const [questions, setQuestions] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [sources, setSources] = useState([]);
  const [difficulties, setDifficulties] = useState([]);
  const [statuses, setStatuses] = useState([]);
  const [tags, setTags] = useState([]);
  const [sortOptions, setSortOptions] = useState([]);
  const [orderOptions, setOrderOptions] = useState([]);


  useEffect(async () => {
    // Get questions
    await fetchForPage(1);

    // Get metadata for filter bar
    const req = {
      method: "GET",
      headers: getReqHeader()
    };

    const metadataQuery = {
      sources: true,
      difficulties: true,
      statuses: true,
      tags: true,
      sort_by: true,
      order: true,
    };

    fetch(`/api/metadata?${formatQueries(metadataQuery)}`, req)
      .then(res => res.json())
      .then(data => {
        setSources(data.sources);
        setDifficulties(data.difficulties);
        setStatuses(data.statuses);
        setTags(data.tags);
        setSortOptions(data.sort_by);
        setOrderOptions(data.order);
      })
      .catch(err => {
        throw err;
      });
  }, []);

  const fetchForPage = async (page, pageSize = null) => {
    let query = { page: page };
    if (pageSize) query = { ...query, per_page: pageSize }
    await searchQuestions(query);
  };

  const searchQuestions = async (query) => {
    const data = await getQuestions(query);
    setQuestions(data.data);
    setPage(data.page);
    setTotalPages(data.pages);
  };

  const getQuestions = async (queries = {}) => {
    const tagsQueryStr = (tags) => {
      if (!Array.isArray(tags)) return ""
      const individualQuery = tags.map(tag => `tags=${tag}`);
      return individualQuery.join("&");
    };

    const req = {
      method: "GET",
      headers: getReqHeader(),
    }

    const t = queries.tags;
    delete queries.tags;
    let queryStr = formatQueries(queries) + "&";
    queryStr += tagsQueryStr(t);

    return await fetch(`/api/questions?${queryStr}`, req)
      .then(res => res.json())
      .catch(err => {
        throw err;
      })
  };

  return (
    <div>
      <FilterBar sources={sources} difficulties={difficulties} statuses={statuses} tags={tags}
        sortOptions={sortOptions} orderOptions={orderOptions} searchQuestions={searchQuestions} />
      <QuestionList questions={questions} />
      <PaginationBoxes page={page} totalPages={totalPages} fetchForPage={fetchForPage} />
    </div>
  );
}
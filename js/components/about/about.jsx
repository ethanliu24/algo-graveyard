import ReactMarkdown from 'react-markdown';
import aboutContent from "../../../README.md?raw";

export default function About() {
    console.log(aboutContent)
    return <ReactMarkdown children={aboutContent} />
}
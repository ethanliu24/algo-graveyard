import Markdown from 'react-markdown';
import about from "../../../README.md?raw";

export default function About() {
    const aboutContent = about.replace("# Algo Graveyard", "").trim();
    return <div className="markdown-content"><Markdown children={aboutContent} /></div>;
}
export default function ExportForm(props) {
    return (
        <div className="flex flex-col justify-start items-start gap-4 w-full">{props.question.title}</div>
    );
}
export default function Loader(props) {
    const dimension = props.dimension ? `w-${props.dimension} h-${props.dimension}` : "w-4 h-4"
    
    return (
        <div className={`rounded-full border-3 border-white/60 border-t-white ${dimension} animate-spin`}>
        </div>
    );
}
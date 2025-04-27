export default function NotFound() {
  return (
		<div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-2/3">
			<div className="flex flex-col justify-center items-center gap-4 w-full h-fit overflow-y-hidden">
				<h1 id="not-found-title" className="text-9xl font-extrabold">Oops!</h1>
				<h2 className="text-base font-bold">404 - PAGE NOT FOUND</h2>
				<p className="text-xs font-light">The page you are looking for doesn't exist or has been removed.</p>
				<button><a href="/">HOME</a></button>
			</div>
		</div>
  );
}
export default function Header() {
  return (
    <div className="rounded-3xl border-1 border-gray-100 p-8 bg-gray-50 shadow-sm max-lg:p-4
      grid grid-cols-[4fr_5fr] grid-rows-[1fr_5fr] gap-x-8 grid-flow-col
      max-lg:grid-cols-1 max-lg:grid-rows-[fit-content(10px)_fit-content(10px)_fit-content(10px)] max-lg:gap-y-1">
      <h2 className="text-2xl max-lg:text-center max-lg:text-base">Algo Graveyard</h2>
      <p className="text-xs font-light max-lg:text-center max-lg:text-[0.7rem]">
        I made a wish to a gennie. I said, "Let me be happy." <br />
        The gennie said, "Sure, but only for a moment." <br />
        I said, "Then let that moment live in my smile." <br />
        He said, "Only for a second." <br />
        I said, "Then let that second be every second I breath." <br />
        He said, "Only once". <br />
        I said, "Then let that once, last forever." <br />
        The genie told me to shut the fuck up. <br />
        <br />
        {/* This has nothing to do with the project. I put this here for decoration. */}
        神说，诸水之间要有空气。多放大悲咒，积阳德。每日播放大悲咒，积积阳阳德。
        May my disappointingly inefficent algorithms rest in peace.
      </p>
      <img src="./static/res/ghost.png" alt="crazy gpt generated ghost"
        className="rounded-2xl brightness-110 w-[100%] shadow-md row-span-2 my-auto max-lg:row-span-1 max-lg:mt-3" />
    </div>
  );
}

export default function Home() {


  return (
    <div
    className="container px-4 mx-auto pt-12 bg-cover bg-center bg-no-repeat"
    >
    <div className="flex flex-wrap items-center -mx-4 bg-white bg-opacity-80 p-6 rounded-lg">
        <div className="w-full md:w-1/2 px-4 mb-6 md:mb-0">
        <span className="font-semibold text-xs text-blue-400">What's new at Shuffle</span>
        <h2 className="mt-8 mb-6 lg:mb-12 text-4xl lg:text-5xl font-semibold font-heading">
            Take care of your performance every day.
        </h2>
        <div className="max-w-lg mb-6 lg:mb-12">
            <p className="text-xl text-gray-500">
            Build a well-presented brand that everyone will love. Take care to develop resources continually and integrate them with previous projects.
            </p>
        </div>
        <div className="flex flex-wrap">
            <a
            className="inline-block px-6 py-4 mb-3 mr-4 text-sm font-medium leading-normal bg-red-400 hover:bg-red-300 text-white rounded transition duration-200"
            href="#"
            >
            Track your performance
            </a>
            <a
            className="inline-block px-6 py-4 mb-3 text-sm font-medium leading-normal hover:text-gray-700 rounded border"
            href="#"
            >
            Learn More
            </a>
        </div>
        </div>
        <div className="relative w-full md:w-1/2 px-4">
        <img className="relative" src="/no_pic.jpg" alt="" />
        </div>
    </div>
    </div>

  )
}
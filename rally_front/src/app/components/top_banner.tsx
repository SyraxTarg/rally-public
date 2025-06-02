interface TopBannerProps{
  headline: string;
  text: string;
  buttonText: string;
  buttonLink: string;
  height: string;
  maxHeight: string;
  backgroundColor: string;
  closeButtonClicked: () => void;
  buttonBackgroundColor: string;
}

export default function TopBanner({
  headline,
  text,
  buttonText,
  buttonLink,
  height,
  maxHeight,
  backgroundColor,
  closeButtonClicked,
  buttonBackgroundColor,
}: TopBannerProps) {
  return (
    <div
      className="w-full flex items-center justify-center p-4 shadow-md"
      style={{
        backgroundColor: backgroundColor || "#fecaca",
        height: height || "auto",
        maxHeight: maxHeight || "350px",
      }}
    >
      <div className="relative flex flex-col items-center w-full max-w-5xl">
        {/* Bouton fermer */}
        <button
          className="absolute top-2 right-2 text-lg font-bold text-black hover:text-red-600"
          onClick={closeButtonClicked}
        >
          ×
        </button>

        {/* Contenu */}
        <div className="flex flex-col items-center text-center gap-3 w-full">
          <div className="flex flex-col items-center gap-2">
            <h4 className="text-lg font-bold uppercase">{headline}</h4>
            <div
              className="text-sm md:text-base"
              dangerouslySetInnerHTML={{ __html: text }}
            />
          </div>

          <a
            href={buttonLink}
            className="px-4 py-2 rounded text-white font-semibold"
            style={{
              backgroundColor: buttonBackgroundColor || "#f87171",
            }}
          >
            {buttonText}
          </a>
        </div>
      </div>
    </div>
  );
}

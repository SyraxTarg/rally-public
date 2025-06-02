type AvatarProps = {
    src?: string;
    alt?: string;
  };

  export default function Avatar({ src, alt = "Avatar" }: AvatarProps) {
    return (
      <img
        src={src || "/pfps/default.jpg"}
        alt={alt}
        className="
          rounded-full
          object-cover
          cursor-pointer
          transition-transform duration-200
          hover:scale-105
          w-5 h-5
          sm:w-6 sm:h-6
          md:w-7 md:h-7
          lg:w-8 lg:h-8
          xl:w-10 xl:h-10
        "
      />
    );
  }

import styles from "./auth_button.module.css"

export default function AuthButton({text, isLoading}){
    return(
        <div>
          <button
            type="submit"
            disabled={isLoading}
            className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 ${styles.auth_button}`}
          >
            {text}
          </button>
        </div>
    )
}
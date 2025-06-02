import NextAuth from "next-auth"
import CredentialsProvider from "next-auth/providers/credentials"

export default NextAuth({
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        const res = await fetch("http://localhost:8000/api/v1/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: credentials?.email,
            password: credentials?.password,
          }),
        });

        const data = await res.json();

        if (res.ok && data.access_token) {
          return {
            email: credentials?.email,
            access_token: data.access_token,
            refresh_token: data.refresh_token,
          };
        }

        throw new Error(data.detail || "Login failed");
      }
    })
  ],
  session: {
    strategy: "jwt"
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.access_token = user.access_token;
        token.refresh_token = user.refresh_token;
        token.email = user.email;
      }
      return token;
    },
    async session({ session, token }) {
      session.user = {
        email: token.email,
      };
      session.access_token = token.access_token;
      session.refresh_token = token.refresh_token;
      return session;
    }
  },
  pages: {
    signIn: "/auth/login",
  }
});

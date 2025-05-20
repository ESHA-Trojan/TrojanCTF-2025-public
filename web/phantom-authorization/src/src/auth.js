import NextAuth from 'next-auth';
import { authConfig } from './auth.config';

// Export auth, signIn, and signOut from NextAuth using your config
export const { auth, signIn, signOut } = NextAuth({
  ...authConfig,
});

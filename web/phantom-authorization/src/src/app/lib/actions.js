'use server';

import { signIn } from '@/auth';

// ...

export async function authenticate(prevState, formData) {
  try {
    await signIn('credentials', formData);
  } catch (error) {
    return 'Invalid credentials.';
  }
}

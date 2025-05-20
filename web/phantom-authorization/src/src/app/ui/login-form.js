'use client';

import {
  AtSymbolIcon,
  KeyIcon,
  ExclamationCircleIcon,
} from '@heroicons/react/24/outline';
import { ArrowRightIcon } from '@heroicons/react/20/solid';
import { Button } from '@/app/ui/button';
import { useActionState } from 'react';
import { authenticate } from '@/app/lib/actions';
import { useSearchParams } from 'next/navigation';

export default function LoginForm() {
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get('callbackUrl') || '/dashboard';
  const [errorMessage, formAction, isPending] = useActionState(
    authenticate,
    undefined
  );

  return (
    <form action={formAction} className="space-y-3 w-full">
      <div>
        <label
          className="mb-3 mt-5 block text-xs font-medium text-gray-200"
          htmlFor="email"
        >
          Username
        </label>
        <div className="relative">
          <input
            className="peer block w-full rounded-md border border-gray-800 bg-transparent py-[9px] pl-10 text-sm text-white outline-1 placeholder:text-gray-400 outline-gray-500"
            id="username"
            type="username"
            name="username"
            placeholder="Enter your username"
            required
          />
          <AtSymbolIcon className="pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-400 peer-focus:text-white" />
        </div>
      </div>
      <div>
        <label
          className="mb-3 mt-5 block text-xs font-medium text-gray-200"
          htmlFor="password"
        >
          Password
        </label>
        <div className="relative">
          <input
            className="peer block w-full rounded-md border border-gray-800 bg-transparent py-[9px] pl-10 text-sm text-white outline-1 outline-gray-500 placeholder:text-gray-400"
            id="password"
            type="password"
            name="password"
            placeholder="Enter password"
            required
          />
          <KeyIcon className="pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-400 peer-focus:text-white" />
        </div>
      </div>
      <input type="hidden" name="redirectTo" value={callbackUrl} />
      <Button className="mt-4 w-full" aria-disabled={isPending}>
        Log in
      </Button>
      <div
        className="flex h-8 items-end space-x-1"
        aria-live="polite"
        aria-atomic="true"
      >
        {errorMessage && (
          <>
            <ExclamationCircleIcon className="h-5 w-5 text-red-500" />
            <p className="text-sm text-red-500">{errorMessage}</p>
          </>
        )}
      </div>
    </form>
  );
}

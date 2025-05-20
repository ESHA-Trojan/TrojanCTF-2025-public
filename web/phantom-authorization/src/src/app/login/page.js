import logo from '@/app/ui/logo.png';
import Image from 'next/image';
import LoginForm from '@/app/ui/login-form';
import { Suspense } from 'react';

export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-black">
      <div className="mx-auto w-full max-w-md rounded-2xl bg-[#0D3C42] shadow-xl p-8 flex flex-col items-center space-y-6">
        <div className="flex flex-col items-center space-y-2">
          <div className="rounded-full p-2 shadow-inner">
            <Image
              src={logo}
              alt="Logo"
              width={126.5}
              height={144}
              className="rounded-full object-contain"
              priority
            />
          </div>
          <h1 className="text-2xl font-bold text-gray-200 tracking-tight">
            Please log in to continue.
          </h1>
          <p className="text-gray-400 text-sm">Sign in to your account</p>
        </div>
        <Suspense fallback={<div>Loading...</div>}>
          <div style={{ width: '90%', height: '90%', margin: 'auto' }}>
            <LoginForm />
          </div>
        </Suspense>
      </div>
    </main>
  );
}

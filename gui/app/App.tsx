"use client";

import { Geist, Geist_Mono } from "next/font/google";
import { Menu } from "./components/Sidebar";
import { Bounce, ToastContainer } from "react-toastify";
import { Suspense } from "react";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

type APPProps = {
  children: React.ReactNode;
};

export const App = ({ children }: APPProps) => {
  return (
    <body
      className={`${geistSans.variable} ${geistMono.variable} antialiased flex h-screen overflow-hidden`}
    >
      <Menu></Menu>
      <div className="p-2 overflow-auto w-full">
        <Suspense>{children}</Suspense>
      </div>
      <ToastContainer
        position="bottom-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick={false}
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="colored"
        transition={Bounce}
      />
    </body>
  );
};

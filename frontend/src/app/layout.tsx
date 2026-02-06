import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "مُتَحَكِّم الذكي | Mutahakkim-AI - المنظومة الذاتية لحواسيب الذكاء الاصطناعي",
  description: "المنظومة الذاتية لأتمتة الأنظمة وتطبيقات الويب بحواسيب الذكاء الاصطناعي والاستدلال الحتمي (Computer-Use Deterministic Runtime)",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ar" dir="rtl">
      <body className="antialiased bg-[#030712] text-slate-100 min-h-screen">
        {children}
      </body>
    </html>
  );
}

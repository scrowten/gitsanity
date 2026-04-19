import { Telescope, Star, Sparkles, BookMarked } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function HomePage() {
  const loginUrl = `${API_URL}/auth/login`;

  return (
    <main className="min-h-screen bg-[#f6f8fa]">
      {/* Nav */}
      <nav className="bg-[#161b22] border-b border-[#30363d]">
        <div className="max-w-4xl mx-auto px-4 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2 font-bold text-white">
            <Telescope className="w-5 h-5 text-[#2da44e]" />
            GitSanity
          </div>
          <a
            href={loginUrl}
            className="px-4 py-1.5 text-sm font-medium text-white bg-[#2da44e] rounded-md hover:bg-[#2c974b] transition-colors"
          >
            Sign in with GitHub
          </a>
        </div>
      </nav>

      {/* Hero */}
      <section className="max-w-3xl mx-auto px-4 pt-20 pb-16 text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#ddf4ff] text-[#0969da] text-sm font-medium mb-6">
          <Sparkles className="w-4 h-4" />
          Like arxiv-sanity, but for GitHub
        </div>

        <h1 className="text-5xl font-bold text-[#1f2328] leading-tight mb-5">
          Discover GitHub repos
          <br />
          <span className="text-[#2da44e]">you&apos;ll actually use</span>
        </h1>

        <p className="text-xl text-[#656d76] mb-10 max-w-xl mx-auto">
          GitSanity learns from your GitHub stars and surfaces repositories you
          would never find on your own — beyond simple trending lists.
        </p>

        <a
          href={loginUrl}
          className="inline-flex items-center gap-2 px-6 py-3 text-base font-semibold text-white bg-[#2da44e] rounded-md hover:bg-[#2c974b] transition-colors shadow-sm"
        >
          <svg viewBox="0 0 16 16" className="w-5 h-5 fill-current">
            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" />
          </svg>
          Sign in with GitHub — it&apos;s free
        </a>

        <p className="mt-4 text-sm text-[#656d76]">
          We only read your public stars. No write access.
        </p>
      </section>

      {/* Features */}
      <section className="max-w-4xl mx-auto px-4 pb-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <FeatureCard
            icon={<Star className="w-6 h-6 fill-yellow-400 text-yellow-400" />}
            title="Built from your stars"
            description="Sign in with GitHub and we instantly analyze your starred repos to build your preference profile."
          />
          <FeatureCard
            icon={<Sparkles className="w-6 h-6 text-[#2da44e]" />}
            title="Personalized feed"
            description="Get a daily feed of repos matched to your languages, topics, and interests — not just trending."
          />
          <FeatureCard
            icon={<BookMarked className="w-6 h-6 text-[#0969da]" />}
            title="Save for later"
            description="Bookmark repos you want to explore. Dismiss ones that don't fit. The feed learns from both."
          />
        </div>
      </section>
    </main>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="bg-white rounded-md border border-[#d0d7de] p-6">
      <div className="mb-3">{icon}</div>
      <h3 className="font-semibold text-[#1f2328] mb-1">{title}</h3>
      <p className="text-sm text-[#656d76]">{description}</p>
    </div>
  );
}

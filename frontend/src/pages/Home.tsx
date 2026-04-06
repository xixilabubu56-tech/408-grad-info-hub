import { Link, useNavigate } from 'react-router-dom'
import { useEffect, useMemo, useState } from 'react'
import { ArrowRight, Building2, GraduationCap, School, Search } from 'lucide-react'
import { apiUrl } from '../lib/api'

interface SummaryResponse {
  institutionCount: number
  majorCount: number
  collegeCount: number
  noticeCount: number
  provinceCount: number
  latestYear: number | null
  latestNoticeDate: string | null
  topInstitutions: Array<{
    id: number
    name: string
    ranking: number
  }>
}

export default function Home() {
  const navigate = useNavigate()
  const [search, setSearch] = useState('')
  const [summary, setSummary] = useState<SummaryResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    const controller = new AbortController()

    fetch(apiUrl('/api/summary'), { signal: controller.signal })
      .then((res) => {
        if (!res.ok) {
          throw new Error('summary request failed')
        }
        return res.json()
      })
      .then((data: SummaryResponse) => {
        setSummary(data)
        setError(false)
        setLoading(false)
      })
      .catch(() => {
        setError(true)
        setLoading(false)
      })

    return () => controller.abort()
  }, [])

  const handleSearch = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && search.trim()) {
      navigate(`/institutions?q=${encodeURIComponent(search.trim())}`)
    }
  }

  const stats = useMemo(
    () => [
      {
        label: '院校',
        value: summary?.institutionCount ?? '--',
        icon: School,
      },
      {
        label: '招生学院',
        value: summary?.collegeCount ?? '--',
        icon: Building2,
      },
      {
        label: '招生专业',
        value: summary?.majorCount ?? '--',
        icon: GraduationCap,
      },
      {
        label: '官方通知',
        value: summary?.noticeCount ?? '--',
        icon: Search,
      },
    ],
    [summary],
  )

  const quickKeywords = ['清华大学', '北京邮电大学', '西安电子科技大学', '电子信息', '网络空间安全']

  return (
    <main className="w-full flex-1 flex flex-col items-center pt-24 px-4 pb-16">
      <section className="w-full max-w-6xl rounded-[2rem] border border-white/60 bg-[radial-gradient(circle_at_top_left,_rgba(96,165,250,0.18),_transparent_35%),linear-gradient(180deg,_rgba(255,255,255,0.92),_rgba(255,255,255,0.72))] dark:border-gray-800 dark:bg-[radial-gradient(circle_at_top_left,_rgba(59,130,246,0.22),_transparent_30%),linear-gradient(180deg,_rgba(28,28,30,0.95),_rgba(10,10,12,0.95))] backdrop-blur-xl shadow-[0_24px_80px_rgba(15,23,42,0.08)] p-8 md:p-12">
        <div className="max-w-3xl">
          <div className="inline-flex items-center gap-2 rounded-full bg-white/70 dark:bg-white/5 px-4 py-2 text-sm text-gray-600 dark:text-gray-300 border border-gray-200/80 dark:border-gray-800 mb-6">
            仅收录统考 408 相关院校、学院、专业与官方通知
          </div>
          <h1 className="text-5xl md:text-7xl font-semibold tracking-tight mb-6 leading-[1.05]">
            统考 408，<br />一站式查全。
          </h1>
          <p className="text-lg md:text-2xl text-gray-500 max-w-2xl mb-10">
            覆盖院校排名、学院官网、复试线、复录比、历年分数与官方通知，减少在多个学校官网之间来回切换。
          </p>

          <div className="w-full max-w-2xl relative mb-6">
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={handleSearch}
              placeholder="搜索院校、省份或学院关键词，按回车直接进入结果页"
              className="w-full h-15 pl-13 pr-32 rounded-full bg-white/90 dark:bg-[#1c1c1e] shadow-sm border border-gray-200 dark:border-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 text-base md:text-lg transition"
            />
            <Search className="absolute left-5 top-4.5 w-6 h-6 text-gray-400" />
            <button
              type="button"
              onClick={() => search.trim() && navigate(`/institutions?q=${encodeURIComponent(search.trim())}`)}
              className="absolute right-2 top-2 h-11 px-5 rounded-full bg-black text-white dark:bg-white dark:text-black text-sm font-medium hover:opacity-85 transition"
            >
              立即搜索
            </button>
          </div>

          <div className="flex flex-wrap gap-3 text-sm text-gray-500">
            {quickKeywords.map((keyword) => (
              <button
                key={keyword}
                type="button"
                onClick={() => navigate(`/institutions?q=${encodeURIComponent(keyword)}`)}
                className="rounded-full bg-white/70 dark:bg-white/5 px-3 py-1.5 border border-gray-200 dark:border-gray-800 hover:opacity-80 transition"
              >
                {keyword}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-10">
          {stats.map((item) => {
            const Icon = item.icon
            return (
              <div
                key={item.label}
                className="rounded-[1.75rem] bg-white/80 dark:bg-white/4 border border-gray-100 dark:border-gray-800 p-5"
              >
                <div className="w-10 h-10 rounded-2xl bg-gray-100 dark:bg-gray-900 flex items-center justify-center mb-4">
                  <Icon className="w-5 h-5 text-gray-600 dark:text-gray-300" />
                </div>
                <div className="text-3xl font-semibold tracking-tight">{loading ? '--' : item.value}</div>
                <div className="text-sm text-gray-500 mt-2">{item.label}</div>
              </div>
            )
          })}
        </div>
      </section>

      <section className="w-full max-w-6xl mt-10 grid grid-cols-1 lg:grid-cols-[1.2fr_0.8fr] gap-6">
        <div className="bg-white dark:bg-[#1c1c1e] p-8 rounded-[2rem] shadow-sm border border-gray-100 dark:border-gray-800">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-2xl font-semibold tracking-tight">核心功能</h2>
              <p className="text-gray-500 mt-2">围绕 408 考生决策链路设计，优先提供真正能用的数据入口。</p>
            </div>
            <Link to="/institutions" className="inline-flex items-center text-sm font-medium text-blue-500 hover:opacity-70 transition">
              浏览全部院校 <ArrowRight className="w-4 h-4 ml-1" />
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Link to="/institutions" className="rounded-[1.5rem] border border-gray-100 dark:border-gray-800 bg-gray-50/80 dark:bg-black/30 p-6 hover:-translate-y-0.5 hover:shadow-sm transition">
              <h3 className="text-lg font-semibold mb-3">院校排名检索</h3>
              <p className="text-sm text-gray-500">按排名浏览全国重点 408 招生院校，快速查看学校层级与地区分布。</p>
            </Link>
            <Link to="/institutions" className="rounded-[1.5rem] border border-gray-100 dark:border-gray-800 bg-gray-50/80 dark:bg-black/30 p-6 hover:-translate-y-0.5 hover:shadow-sm transition">
              <h3 className="text-lg font-semibold mb-3">学院官网直达</h3>
              <p className="text-sm text-gray-500">每个专业都可直接跳转到对应学院官网或研究生院主页，减少无效查找。</p>
            </Link>
            <Link to="/institutions" className="rounded-[1.5rem] border border-gray-100 dark:border-gray-800 bg-gray-50/80 dark:bg-black/30 p-6 hover:-translate-y-0.5 hover:shadow-sm transition">
              <h3 className="text-lg font-semibold mb-3">历年数据汇总</h3>
              <p className="text-sm text-gray-500">展示复试线、最高分、最低分、复试人数、录取人数与复录比。</p>
            </Link>
          </div>
        </div>

        <div className="bg-white dark:bg-[#1c1c1e] p-8 rounded-[2rem] shadow-sm border border-gray-100 dark:border-gray-800">
          <h2 className="text-2xl font-semibold tracking-tight mb-3">当前覆盖</h2>
          <p className="text-gray-500 mb-6">
            {summary?.latestYear ? `已整理到 ${summary.latestYear} 年数据，优先展示排名靠前院校。` : '正在同步最新院校数据。'}
          </p>
          {summary && (
            <div className="grid grid-cols-2 gap-3 mb-6">
              <div className="rounded-2xl bg-gray-50 dark:bg-black/30 px-4 py-4">
                <div className="text-sm text-gray-500">覆盖省份</div>
                <div className="text-2xl font-semibold mt-1">{summary.provinceCount}</div>
              </div>
              <div className="rounded-2xl bg-gray-50 dark:bg-black/30 px-4 py-4">
                <div className="text-sm text-gray-500">最近通知日期</div>
                <div className="text-sm md:text-base font-semibold mt-2">{summary.latestNoticeDate ?? '待补充'}</div>
              </div>
            </div>
          )}
          <div className="space-y-3">
            {(summary?.topInstitutions ?? []).map((institution) => (
              <Link
                key={institution.id}
                to={`/institution/${institution.id}`}
                className="flex items-center justify-between rounded-2xl border border-gray-100 dark:border-gray-800 px-4 py-4 hover:bg-gray-50 dark:hover:bg-white/5 transition"
              >
                <div>
                  <div className="text-sm text-gray-500">排名 #{institution.ranking}</div>
                  <div className="font-medium mt-1">{institution.name}</div>
                </div>
                <ArrowRight className="w-4 h-4 text-gray-400" />
              </Link>
            ))}
            {!loading && !summary?.topInstitutions?.length && (
              <div className="rounded-2xl border border-dashed border-gray-200 dark:border-gray-800 px-4 py-6 text-sm text-gray-500">
                暂无摘要数据，请先启动后端并完成数据导入。
              </div>
            )}
            {error && (
              <div className="rounded-2xl border border-amber-200 bg-amber-50 text-amber-700 px-4 py-4 text-sm">
                摘要接口暂时不可用，请确认后端已启动，或稍后刷新页面重试。
              </div>
            )}
          </div>
        </div>
      </section>
    </main>
  )
}

import { useEffect, useMemo, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, BookOpen, Calendar, ExternalLink, Globe, School, Users } from 'lucide-react'
import { apiUrl } from '../lib/api'

interface MajorHistory {
  year: number
  score_line: number | null
  highest: number | null
  lowest: number | null
  average: number | null
  retest_count: number | null
  admitted: number | null
  retest_ratio: string | null
}

interface Major {
  id: number
  college_name: string | null
  college_website: string | null
  major_name: string
  degree_type: string
  study_mode: string
  exam_subjects: string
  history: MajorHistory[]
}

interface InstitutionDetailResponse {
  id: number
  name: string
  province: string
  city?: string
  ranking: number
  is985: boolean
  is211: boolean
  isDoubleFirstClass: boolean
  official_website?: string | null
  grad_website?: string | null
  description?: string | null
  colleges: string[]
  stats: {
    majorCount: number
    collegeCount: number
    noticeCount: number
  }
  majors: Major[]
  notices: Array<{
    id: number
    title: string
    category: string | null
    date: string | null
    url: string
  }>
}

export default function InstitutionDetail() {
  const { id } = useParams()
  const [data, setData] = useState<InstitutionDetailResponse | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(apiUrl(`/api/institutions/${id}`))
      .then(res => {
        if (!res.ok) throw new Error("API failed");
        return res.json()
      })
      .then(result => {
        setData(result)
        setLoading(false)
      })
      .catch(err => {
        console.error("Fetch Detail Error:", err)
        setLoading(false)
      })
  }, [id])

  const statItems = useMemo(
    () => [
      { label: '招生学院', value: data?.stats.collegeCount ?? 0, icon: School },
      { label: '招生专业', value: data?.stats.majorCount ?? 0, icon: BookOpen },
      { label: '官方通知', value: data?.stats.noticeCount ?? 0, icon: Calendar },
    ],
    [data],
  )

  const latestYear = useMemo(() => {
    if (!data) return null
    const years = data.majors.flatMap((major) => major.history.map((item) => item.year))
    return years.length ? Math.max(...years) : null
  }, [data])

  if (loading) {
    return (
      <div className="w-full min-h-screen flex justify-center items-center text-gray-400 pt-24">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 dark:border-white mr-3"></div>
        正在加载院校详细数据...
      </div>
    )
  }

  if (!data) {
    return (
      <div className="w-full min-h-screen flex flex-col justify-center items-center text-gray-400 pt-24 gap-4">
        <p>未能找到该院校的数据或后端接口未启动</p>
        <Link to="/institutions" className="text-blue-500 hover:underline">返回院校列表</Link>
      </div>
    )
  }

  return (
    <div className="w-full flex-1 flex flex-col items-center pt-24 px-4 pb-20">
      <div className="w-full max-w-6xl">
        <Link to="/institutions" className="inline-flex items-center text-blue-500 hover:opacity-70 transition mb-6 font-medium">
          <ArrowLeft className="w-4 h-4 mr-1" />
          返回院校大全
        </Link>

        <div className="bg-white dark:bg-[#1c1c1e] p-8 rounded-[2rem] shadow-sm border border-gray-100 dark:border-gray-800 mb-8">
          <div className="flex flex-col xl:flex-row xl:items-start xl:justify-between gap-6 mb-8">
            <div className="max-w-3xl">
              <div className="inline-flex items-center rounded-full bg-gray-100 dark:bg-gray-800 px-3 py-1 text-sm text-gray-500 mb-4">
                全国排名 #{data.ranking}
              </div>
              <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-3">{data.name}</h1>
              <p className="text-gray-500 text-lg">
                {data.province}{data.city && data.city !== data.province ? ` · ${data.city}` : ''} · 仅展示统考 408 相关学院与专业
              </p>
              {data.description && (
                <p className="text-gray-500 mt-4 leading-7">{data.description}</p>
              )}
            </div>
            <div className="flex flex-col gap-3 min-w-[240px]">
              {data.grad_website && (
                <a href={data.grad_website} target="_blank" rel="noreferrer" className="inline-flex items-center justify-center px-4 py-3 bg-black dark:bg-white text-white dark:text-black rounded-full text-sm font-medium hover:opacity-80 transition">
                  访问研究生院主站 <ExternalLink className="w-4 h-4 ml-1" />
                </a>
              )}
              {data.official_website && (
                <a href={data.official_website} target="_blank" rel="noreferrer" className="inline-flex items-center justify-center px-4 py-3 bg-gray-100 dark:bg-gray-800 rounded-full text-sm font-medium hover:opacity-80 transition">
                  访问学校招生主页 <Globe className="w-4 h-4 ml-1" />
                </a>
              )}
            </div>
          </div>

          <div className="flex flex-wrap gap-2 mb-6">
            {data.is985 && <span className="px-3 py-1 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 text-sm font-medium rounded-full">985 工程</span>}
            {data.is211 && <span className="px-3 py-1 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 text-sm font-medium rounded-full">211 工程</span>}
            {data.isDoubleFirstClass && (
              <span className="px-3 py-1 bg-purple-50 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400 text-sm font-medium rounded-full">双一流</span>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            {statItems.map((item) => {
              const Icon = item.icon
              return (
                <div key={item.label} className="rounded-[1.5rem] bg-gray-50 dark:bg-black/30 p-5">
                  <div className="w-10 h-10 rounded-2xl bg-white dark:bg-gray-900 flex items-center justify-center mb-4">
                    <Icon className="w-5 h-5 text-gray-500" />
                  </div>
                  <div className="text-3xl font-semibold">{item.value}</div>
                  <div className="text-sm text-gray-500 mt-2">{item.label}</div>
                </div>
              )
            })}
          </div>

          <div className="rounded-[1.5rem] bg-gray-50 dark:bg-black/30 p-5">
            <div className="text-sm text-gray-500 mb-3">已覆盖招生学院</div>
            <div className="flex flex-wrap gap-2">
              {data.colleges.length > 0 ? (
                data.colleges.map((college) => (
                  <span key={college} className="px-3 py-1.5 rounded-full bg-white dark:bg-gray-900 text-sm border border-gray-200 dark:border-gray-800">
                    {college}
                  </span>
                ))
              ) : (
                <span className="text-sm text-gray-400">暂未整理学院列表</span>
              )}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-8">
            <h2 className="text-2xl font-bold flex items-center"><BookOpen className="w-6 h-6 mr-2" /> 开设的 408 统考专业/学院</h2>
            
            {data.majors && data.majors.length > 0 ? data.majors.map((major) => (
              <div key={major.id} className="bg-white dark:bg-[#1c1c1e] p-6 rounded-[2rem] shadow-sm border border-gray-100 dark:border-gray-800">
                <div className="mb-4 flex justify-between items-start">
                  <div>
                    <h3 className="text-xl font-bold text-blue-600 dark:text-blue-400">{major.major_name} <span className="text-sm font-normal text-gray-500 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-md ml-2">{major.degree_type === 'academic' ? '学硕' : '专硕'}</span></h3>
                    <p className="text-gray-500 text-sm mt-1">{major.college_name} · {major.study_mode === 'full_time' ? '全日制' : '非全日制'}</p>
                  </div>
                  {major.college_website && (
                    <a href={major.college_website} target="_blank" rel="noreferrer" className="inline-flex items-center px-3 py-1.5 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-full text-xs font-medium hover:bg-blue-100 dark:hover:bg-blue-900/40 transition flex-shrink-0">
                      前往学院官网 <ExternalLink className="w-3 h-3 ml-1" />
                    </a>
                  )}
                </div>
                
                <div className="bg-gray-50 dark:bg-black/50 p-4 rounded-2xl mb-6 text-sm">
                  <span className="font-semibold text-gray-700 dark:text-gray-300">初试科目：</span>
                  <span className="text-gray-600 dark:text-gray-400">{major.exam_subjects}</span>
                </div>

                <h4 className="font-semibold mb-3">历年分数线与复录比</h4>
                {major.history && major.history.length > 0 ? (
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                      <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-800/50 dark:text-gray-400 rounded-t-xl">
                        <tr>
                          <th className="px-4 py-3">年份</th>
                          <th className="px-4 py-3">复试线</th>
                          <th className="px-4 py-3">最高/低分</th>
                          <th className="px-4 py-3">录取平均分</th>
                          <th className="px-4 py-3">复试人数</th>
                          <th className="px-4 py-3">录取人数</th>
                          <th className="px-4 py-3">复录比</th>
                        </tr>
                      </thead>
                      <tbody>
                        {major.history.map((h) => (
                          <tr key={h.year} className="border-b dark:border-gray-800 last:border-0">
                            <td className="px-4 py-3 font-medium text-gray-900 dark:text-white">{h.year}</td>
                            <td className="px-4 py-3 text-red-500 font-semibold">{h.score_line || '待发布'}</td>
                            <td className="px-4 py-3">{h.highest ? `${h.highest} / ${h.lowest}` : '-'}</td>
                            <td className="px-4 py-3">{h.average || '-'}</td>
                            <td className="px-4 py-3">{h.retest_count || '-'}</td>
                            <td className="px-4 py-3">{h.admitted || '-'}</td>
                            <td className="px-4 py-3">{h.retest_ratio || '-'}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p className="text-gray-400 text-sm italic">暂无历年分数线数据</p>
                )}
              </div>
            )) : (
              <div className="bg-white dark:bg-[#1c1c1e] p-8 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-800 text-center text-gray-400">
                该院校暂未收录具体的 408 统考专业详情
              </div>
            )}
          </div>

          <div className="space-y-6">
            <h2 className="text-2xl font-bold flex items-center"><Calendar className="w-6 h-6 mr-2" /> 最新官方通知</h2>
            <div className="bg-white dark:bg-[#1c1c1e] p-6 rounded-[2rem] shadow-sm border border-gray-100 dark:border-gray-800">
              {data.notices && data.notices.length > 0 ? (
                <div className="space-y-4">
                  {data.notices.map((notice) => (
                    <a key={notice.id} href={notice.url} target="_blank" rel="noreferrer" className="block group">
                      <div className="text-xs text-blue-500 font-medium mb-1">{notice.category || '官方通知'} · {notice.date || '日期待补充'}</div>
                      <h4 className="text-gray-900 dark:text-gray-100 font-medium leading-snug group-hover:text-blue-500 transition line-clamp-2">
                        {notice.title}
                      </h4>
                    </a>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-sm">暂无近期通知公告</p>
              )}
            </div>

            <div className="bg-white dark:bg-[#1c1c1e] p-6 rounded-[2rem] shadow-sm border border-gray-100 dark:border-gray-800">
              <h3 className="text-lg font-semibold flex items-center mb-4"><Users className="w-5 h-5 mr-2" /> 使用建议</h3>
              <div className="space-y-3 text-sm text-gray-500 leading-6">
                <p>优先查看目标学院官网与当年复试录取方案，再结合近三年复试线判断波动。</p>
                <p>若同校多个学院都招 408，建议分别比较学院官网、专业代码与复录比差异。</p>
                <p>对复试线接近的院校，可重点关注最高分/最低分区间与录取人数变化。</p>
              </div>
            </div>

            <div className="bg-white dark:bg-[#1c1c1e] p-6 rounded-[2rem] shadow-sm border border-gray-100 dark:border-gray-800">
              <h3 className="text-lg font-semibold mb-4">数据说明</h3>
              <div className="space-y-3 text-sm text-gray-500 leading-6">
                <p>当前页面汇总研究生院主站、学校招生主页与学院官网入口，便于你继续核对官方原文。</p>
                <p>历年数据当前已整理到 {latestYear ?? '最新'} 年，优先覆盖统考 408 招生学院与专业。</p>
                <p>如遇具体年份细则调整，请以学校当年招生简章、复试办法与拟录取公示为准。</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

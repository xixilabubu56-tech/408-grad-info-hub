import { useEffect, useMemo, useState } from 'react'
import type { KeyboardEvent } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { Building2, ChevronRight, GraduationCap, MapPin, School, Search, X } from 'lucide-react'
import { apiUrl } from '../lib/api'

interface Institution {
  id: number
  name: string
  province: string
  city?: string
  ranking: number
  is985: boolean
  is211: boolean
  isDoubleFirstClass: boolean
  majorCount: number
  collegeCount: number
  noticeCount: number
  latestYear: number | null
  sampleMajors: string[]
  tags: string[]
}

export default function Institutions() {
  const [institutions, setInstitutions] = useState<Institution[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)
  const [filterProvince, setFilterProvince] = useState('所在省份 (全部)')
  const [filterType, setFilterType] = useState('院校属性 (全部)')
  const [degreeType, setDegreeType] = useState('学位类型 (全部)')
  const [sortBy, setSortBy] = useState('按排名')
  const [keyword, setKeyword] = useState('')

  const navigate = useNavigate()
  const location = useLocation()
  const queryParams = new URLSearchParams(location.search)
  const searchQuery = queryParams.get('q') || ''

  useEffect(() => {
    setKeyword(searchQuery)
  }, [searchQuery])

  useEffect(() => {
    const query = searchQuery.trim()
    const params = new URLSearchParams()
    params.set('limit', '200')
    if (query) params.set('q', query)
    if (filterProvince !== '所在省份 (全部)') params.set('province', filterProvince)
    if (filterType === '985 工程') params.set('school_type', '985')
    if (filterType === '211 工程') params.set('school_type', '211')
    if (filterType === '双一流') params.set('school_type', 'double_first_class')
    if (degreeType === '学硕') params.set('degree_type', 'academic')
    if (degreeType === '专硕') params.set('degree_type', 'professional')

    const controller = new AbortController()

    fetch(apiUrl(`/api/institutions?${params.toString()}`), { signal: controller.signal })
      .then((res) => {
        if (!res.ok) {
          throw new Error('institutions request failed')
        }
        return res.json()
      })
      .then((data: Institution[]) => {
        setInstitutions(data)
        setError(false)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Fetch Error:', err)
        setError(true)
        setLoading(false)
      })

    return () => controller.abort()
  }, [degreeType, filterProvince, filterType, searchQuery])

  const filteredInstitutions = useMemo(
    () =>
      institutions.filter((inst) => {
        let match = true

        if (keyword.trim()) {
          const value = keyword.trim()
          const fullText = [
            inst.name,
            inst.province,
            inst.city,
            ...(inst.sampleMajors ?? []),
            ...inst.tags,
          ]
            .filter(Boolean)
            .join(' ')
          if (!fullText.includes(value)) {
            match = false
          }
        }

        return match
      }),
    [institutions, keyword],
  )

  const displayInstitutions = useMemo(() => {
    const cloned = [...filteredInstitutions]
    if (sortBy === '按专业数') {
      cloned.sort((a, b) => b.majorCount - a.majorCount || a.ranking - b.ranking)
    } else if (sortBy === '按通知数') {
      cloned.sort((a, b) => b.noticeCount - a.noticeCount || a.ranking - b.ranking)
    } else if (sortBy === '按最新年份') {
      cloned.sort((a, b) => (b.latestYear ?? 0) - (a.latestYear ?? 0) || a.ranking - b.ranking)
    } else {
      cloned.sort((a, b) => a.ranking - b.ranking)
    }
    return cloned
  }, [filteredInstitutions, sortBy])

  const allProvinces = Array.from(new Set(institutions.map((i) => i.province))).sort()

  const handleSearch = () => {
    const value = keyword.trim()
    navigate(value ? `/institutions?q=${encodeURIComponent(value)}` : '/institutions')
  }

  const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <div className="w-full flex-1 flex flex-col items-center pt-24 px-4 pb-20">
      <div className="w-full max-w-6xl">
        <div className="mb-10">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-3">院校大全</h1>
          <p className="text-gray-500 text-lg">
            {searchQuery ? `包含 “${searchQuery}” 的 408 院校检索结果` : '按排名浏览全国重点 408 招生院校、学院与专业入口'}
          </p>
        </div>

        <div className="mb-6 rounded-[2rem] border border-gray-100 dark:border-gray-800 bg-white dark:bg-[#1c1c1e] p-4 md:p-5">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="搜索院校、省份、标签关键词，按回车筛选"
              className="w-full h-12 pl-12 pr-32 rounded-full bg-gray-50 dark:bg-black/30 border border-gray-200 dark:border-gray-800 text-sm md:text-base focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <div className="absolute right-2 top-2 flex items-center gap-2">
              {keyword && (
                <button
                  type="button"
                  onClick={() => {
                    setKeyword('')
                    navigate('/institutions')
                  }}
                  className="w-8 h-8 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center hover:opacity-80 transition"
                >
                  <X className="w-4 h-4 text-gray-500" />
                </button>
              )}
              <button
                type="button"
                onClick={handleSearch}
                className="px-4 h-8 rounded-full bg-black text-white dark:bg-white dark:text-black text-sm font-medium hover:opacity-85 transition"
              >
                搜索
              </button>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-[0.9fr_0.1fr] gap-4 items-start mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div className="rounded-[1.5rem] border border-gray-100 dark:border-gray-800 bg-white dark:bg-[#1c1c1e] px-5 py-4">
              <div className="text-sm text-gray-500">当前结果</div>
              <div className="text-2xl font-semibold mt-2">{loading ? '--' : displayInstitutions.length}</div>
            </div>
            <div className="rounded-[1.5rem] border border-gray-100 dark:border-gray-800 bg-white dark:bg-[#1c1c1e] px-5 py-4">
              <div className="text-sm text-gray-500">累计专业</div>
              <div className="text-2xl font-semibold mt-2">
                {loading ? '--' : displayInstitutions.reduce((sum, item) => sum + item.majorCount, 0)}
              </div>
            </div>
            <div className="rounded-[1.5rem] border border-gray-100 dark:border-gray-800 bg-white dark:bg-[#1c1c1e] px-5 py-4">
              <div className="text-sm text-gray-500">覆盖学院</div>
              <div className="text-2xl font-semibold mt-2">
                {loading ? '--' : displayInstitutions.reduce((sum, item) => sum + item.collegeCount, 0)}
              </div>
            </div>
          </div>
          <div className="rounded-[1.5rem] border border-gray-100 dark:border-gray-800 bg-white dark:bg-[#1c1c1e] p-3 flex flex-wrap gap-3 lg:justify-end">
            <select
              className="px-4 py-2 rounded-full bg-gray-50 dark:bg-black/30 border border-gray-200 dark:border-gray-800 text-sm focus:outline-none"
              value={filterProvince}
              onChange={(e) => setFilterProvince(e.target.value)}
            >
              <option>所在省份 (全部)</option>
              {allProvinces.map((p) => (
                <option key={p}>{p}</option>
              ))}
            </select>
            <select
              className="px-4 py-2 rounded-full bg-gray-50 dark:bg-black/30 border border-gray-200 dark:border-gray-800 text-sm focus:outline-none"
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
            >
              <option>院校属性 (全部)</option>
              <option>985 工程</option>
              <option>211 工程</option>
              <option>双一流</option>
            </select>
            <select
              className="px-4 py-2 rounded-full bg-gray-50 dark:bg-black/30 border border-gray-200 dark:border-gray-800 text-sm focus:outline-none"
              value={degreeType}
              onChange={(e) => setDegreeType(e.target.value)}
            >
              <option>学位类型 (全部)</option>
              <option>学硕</option>
              <option>专硕</option>
            </select>
            <select
              className="px-4 py-2 rounded-full bg-gray-50 dark:bg-black/30 border border-gray-200 dark:border-gray-800 text-sm focus:outline-none"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option>按排名</option>
              <option>按专业数</option>
              <option>按通知数</option>
              <option>按最新年份</option>
            </select>

            {searchQuery && (
              <button
                onClick={() => navigate('/institutions')}
                className="px-4 py-2 rounded-full bg-gray-100 dark:bg-gray-800 text-sm hover:bg-gray-200 transition"
              >
                清除搜索
              </button>
            )}
          </div>
        </div>

        {loading && (
          <div className="w-full py-20 flex justify-center items-center text-gray-400 rounded-[2rem] bg-white dark:bg-[#1c1c1e] border border-gray-100 dark:border-gray-800">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 dark:border-white mr-3"></div>
            正在加载院校数据...
          </div>
        )}

        {!loading && error && (
          <div className="w-full py-14 flex flex-col justify-center items-center text-amber-700 bg-amber-50 rounded-[2rem] border border-amber-200 gap-3">
            <p>院校接口暂时不可用，请确认后端服务和数据库状态。</p>
            <button
              type="button"
              onClick={() => navigate(0)}
              className="px-4 py-2 rounded-full bg-amber-100 hover:bg-amber-200 transition text-sm"
            >
              重新加载
            </button>
          </div>
        )}

        {!loading && !error && displayInstitutions.length === 0 && (
          <div className="w-full py-20 flex flex-col justify-center items-center text-gray-400 bg-white dark:bg-[#1c1c1e] rounded-[2rem] border border-gray-100 dark:border-gray-800">
            <Building2 className="w-16 h-16 mb-4 opacity-50" />
            <p>没有找到符合条件的 408 院校数据。</p>
          </div>
        )}

        {!loading && !error && displayInstitutions.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {displayInstitutions.map((inst) => (
              <div
                key={inst.id}
                onClick={() => navigate(`/institution/${inst.id}`)}
                className="group bg-white dark:bg-[#1c1c1e] p-6 rounded-[2rem] shadow-sm border border-gray-100 dark:border-gray-800 hover:shadow-md hover:-translate-y-1 transition transform cursor-pointer flex flex-col"
              >
                <div className="flex justify-between items-start gap-4 mb-5">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-2xl bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                      <Building2 className="w-6 h-6 text-gray-500" />
                    </div>
                    <div>
                      <div className="text-xs text-gray-400 mb-1">排名 #{inst.ranking}</div>
                      <h2 className="text-xl font-bold group-hover:text-blue-500 transition">{inst.name}</h2>
                      <div className="flex items-center text-sm text-gray-500 mt-1 gap-1">
                        <MapPin className="w-4 h-4" />
                        <span>{inst.province}{inst.city && inst.city !== inst.province ? ` · ${inst.city}` : ''}</span>
                      </div>
                    </div>
                  </div>
                  <ChevronRight className="w-5 h-5 text-gray-300 group-hover:text-blue-500 transition" />
                </div>

                <div className="grid grid-cols-3 gap-3 mb-5">
                  <div className="rounded-2xl bg-gray-50 dark:bg-black/30 p-3">
                    <div className="flex items-center gap-2 text-gray-500 text-xs">
                      <School className="w-4 h-4" />
                      学院
                    </div>
                    <div className="text-lg font-semibold mt-2">{inst.collegeCount}</div>
                  </div>
                  <div className="rounded-2xl bg-gray-50 dark:bg-black/30 p-3">
                    <div className="flex items-center gap-2 text-gray-500 text-xs">
                      <GraduationCap className="w-4 h-4" />
                      专业
                    </div>
                    <div className="text-lg font-semibold mt-2">{inst.majorCount}</div>
                  </div>
                  <div className="rounded-2xl bg-gray-50 dark:bg-black/30 p-3">
                    <div className="flex items-center gap-2 text-gray-500 text-xs">
                      <Building2 className="w-4 h-4" />
                      通知
                    </div>
                    <div className="text-lg font-semibold mt-2">{inst.noticeCount}</div>
                  </div>
                </div>

                <div className="rounded-2xl bg-gray-50 dark:bg-black/30 px-4 py-3 mb-5">
                  <div className="text-xs text-gray-500 mb-2">重点专业方向</div>
                  <div className="flex flex-wrap gap-2">
                    {inst.sampleMajors.map((major) => (
                      <span key={major} className="px-2.5 py-1 rounded-full bg-white dark:bg-gray-900 text-xs border border-gray-200 dark:border-gray-800">
                        {major}
                      </span>
                    ))}
                    {inst.latestYear && (
                      <span className="px-2.5 py-1 rounded-full bg-blue-50 dark:bg-blue-900/20 text-xs text-blue-600 dark:text-blue-400">
                        最新年份 {inst.latestYear}
                      </span>
                    )}
                  </div>
                </div>

                <div className="flex flex-wrap gap-2 mt-auto pt-4 border-t border-gray-100 dark:border-gray-800/50">
                  {inst.is985 && <span className="px-3 py-1 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 text-xs font-medium rounded-full">985</span>}
                  {inst.is211 && <span className="px-3 py-1 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 text-xs font-medium rounded-full">211</span>}
                  {inst.isDoubleFirstClass && <span className="px-3 py-1 bg-purple-50 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400 text-xs font-medium rounded-full">双一流</span>}
                  {inst.tags.map((tag, idx) => (
                    tag !== '985' && tag !== '211' && tag !== '双一流' &&
                    <span key={idx} className="px-3 py-1 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 text-xs font-medium rounded-full">{tag}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

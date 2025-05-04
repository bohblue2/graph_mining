import { useQuery } from '@tanstack/react-query'

type NodeType = {
  id: string;
  type: string;
  code?: string;
  name?: string;
}

type LinkType = {
  source: string;
  target: string;
  value: number;
  type?: string;
}

type GraphDataType = {
  nodes: NodeType[];
  links: LinkType[];
}

function GraphData() {
  const { data, isLoading, error } = useQuery<GraphDataType>({
    queryKey: ['graphData'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/test')
      if (!res.ok) throw new Error('네트워크 오류')
      return res.json()
    }
  })

  if (isLoading) return <div>로딩 중...</div>
  if (error) return <div>에러 발생: {(error as Error).message}</div>

  if (!data) return null

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-2">노드 목록</h2>
      <ul className="mb-4">
        {data.nodes.map((node) => (
          <li key={node.id} className="mb-1">
            <span className="font-semibold">{node.id}</span> ({node.type})
            {node.name && <> - {node.name}</>}
          </li>
        ))}
      </ul>
      <h2 className="text-xl font-bold mb-2">링크 목록</h2>
      <ul>
        {data.links.map((link, idx) => (
          <li key={idx}>
            <span className="font-semibold">{link.source}</span> → <span className="font-semibold">{link.target}</span> (value: {link.value}{link.type && `, type: ${link.type}`})
          </li>
        ))}
      </ul>
    </div>
  )
}

function App() {
  return (
    <>
      <GraphData />
    </>
  )
}

export default App

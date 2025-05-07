import { useQuery } from '@tanstack/react-query'
import { useEffect, useRef, useState } from 'react'
import * as d3 from 'd3'
import { CompanyKeywordGraph, CompanyNode, KeywordNode } from './dto/graph';

// D3에서 사용할 수 있는 노드 타입 (id, name, x, y, fx, fy 포함)
type NodeType =
  (CompanyNode & { id: string; name: string; x?: number; y?: number; fx?: number|null; fy?: number|null }) |
  (KeywordNode & { id: string; name: string; x?: number; y?: number; fx?: number|null; fy?: number|null });

// D3에서 사용할 수 있는 링크 타입
type LinkType = { source: string; target: string; value: number; };

function D3Graph({ data }: { data: CompanyKeywordGraph }) {
  const svgRef = useRef<SVGSVGElement | null>(null)
  const [selectedNode, setSelectedNode] = useState<CompanyNode | KeywordNode | null>(null)

  // D3에서 쓸 수 있도록 id, name, x, y, fx, fy만 추가
  const nodes: NodeType[] = [
    ...data.company_nodes.map(n => ({ ...n, id: n.name, name: n.name })),
    ...data.keyword_nodes.map(n => ({ ...n, id: n.keyword, name: n.keyword }))
  ];
  const links: LinkType[] = data.edges.map(e => ({ ...e, value: e.weight ?? 0 }));

  useEffect(() => {
    if (!data) return

    const width = window.innerWidth
    const height = window.innerHeight

    // D3 force simulation
    const manyBody = d3.forceManyBody().strength(-100);
    const simulation = d3.forceSimulation(nodes as d3.SimulationNodeDatum[])
      .force('link', d3.forceLink<NodeType, LinkType>(links)
        .id((d: NodeType) => d.id)
        .distance(120)
        .strength((link: LinkType) => link.value))
      .force('charge', manyBody)
      .force('center', d3.forceCenter(width / 2, height / 2))

    // SVG 초기화
    const svg = d3.select(svgRef.current) as d3.Selection<SVGSVGElement, unknown, null, undefined>
    svg.selectAll('*').remove()

    // 줌/팬 그룹 생성
    const g = svg.append('g')

    // 링크
    const link = g.append('g')
      .selectAll('line')
      .data(links)
      .enter()
      .append('line')
      .attr('stroke', '#7dd3fc')
      .attr('stroke-width', (d: LinkType) => 1 + (d.value ?? 0) * 5)
      .attr('opacity', (d: LinkType) => 0.2 + (d.value ?? 0) * 0.8)

    // 노드
    const nodeGroup = g.append('g')
      .attr('stroke', '#fff')
      .attr('stroke-width', 1.5)
      .selectAll('g')
      .data(nodes)
      .enter()
      .append('g');

    // 회사: rect, 키워드: circle
    nodeGroup.each(function(d: NodeType) {
      const group = d3.select(this);
      if (d.type === 'company') {
        group.append('rect')
          .attr('x', -32)
          .attr('y', -20)
          .attr('width', 64)
          .attr('height', 40)
          .attr('rx', 8)
          .attr('fill', '#7dd3fc');
      } else {
        group.append('circle')
          .attr('r', 24)
          .attr('fill', '#fbbf24');
      }
    });

    nodeGroup
      .on('click', (event: MouseEvent, d: NodeType) => {
        setSelectedNode(d)
      })
      .call(d3.drag<SVGGElement, NodeType>()
        .on('start', (event: d3.D3DragEvent<SVGGElement, NodeType, unknown>, d: NodeType) => {
          manyBody.strength(-10);
          if (!event.active) simulation.alphaTarget(0.3).restart()
          d.fx = d.x
          d.fy = d.y
        })
        .on('drag', (event: d3.D3DragEvent<SVGGElement, NodeType, unknown>, d: NodeType) => {
          d.fx = event.x
          d.fy = event.y
        })
        .on('end', (event: d3.D3DragEvent<SVGGElement, NodeType, unknown>, d: NodeType) => {
          manyBody.strength(-30);
          if (!event.active) simulation.alphaTarget(0)
          d.fx = null
          d.fy = null
        })
      );

    // 노드 라벨
    const label = g.append('g')
      .selectAll('text')
      .data(nodes)
      .enter()
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', 5)
      .attr('font-size', 13)
      .attr('pointer-events', 'none')
      .text((d: NodeType) => d.name ? d.name : d.id)

    // 줌 핸들러
    svg.call(
      d3.zoom<SVGSVGElement, unknown>()
        .scaleExtent([0.1, 10])
        .on('zoom', (event: d3.D3ZoomEvent<SVGSVGElement, unknown>) => {
          g.attr('transform', event.transform.toString())
        })
    )

    simulation.on('tick', () => {
      link
        .attr('x1', (d: d3.SimulationLinkDatum<NodeType>) => (typeof d.source === 'object' ? d.source.x ?? 0 : 0))
        .attr('y1', (d: d3.SimulationLinkDatum<NodeType>) => (typeof d.source === 'object' ? d.source.y ?? 0 : 0))
        .attr('x2', (d: d3.SimulationLinkDatum<NodeType>) => (typeof d.target === 'object' ? d.target.x ?? 0 : 0))
        .attr('y2', (d: d3.SimulationLinkDatum<NodeType>) => (typeof d.target === 'object' ? d.target.y ?? 0 : 0))

      nodeGroup
        .attr('transform', (d: NodeType) => `translate(${d.x ?? 0},${d.y ?? 0})`)

      label
        .attr('x', (d: NodeType) => d.x ?? 0)
        .attr('y', (d: NodeType) => d.y ?? 0)
    })

    // cleanup
    return () => {
      simulation.stop()
    }
  }, [data])

  return (
    <div className="flex justify-center items-center" style={{ width: '100vw', height: '100vh', background: '#181f2a' }}>
      <svg ref={svgRef} width="100vw" height="100vh" style={{ width: '100vw', height: '100vh', border: 'none', background: '#232b3a', display: 'block' }} />
      {selectedNode ? (
        <div style={{
          position: 'fixed',
          right: 32,
          bottom: 32,
          minWidth: 260,
          background: 'rgba(30,36,50,0.85)',
          border: '1px solid #2d3748',
          borderRadius: 16,
          boxShadow: '0 4px 24px rgba(0,0,0,0.25)',
          padding: 24,
          zIndex: 1000,
          color: '#f1f5fa',
          backdropFilter: 'blur(8px)',
        }}>
          <div style={{fontWeight: 'bold', fontSize: 20, marginBottom: 10, color: '#7dd3fc'}}>{(selectedNode as NodeType).name}</div>
          <div style={{marginBottom: 4}}><b>ID:</b> {(selectedNode as NodeType).id}</div>
          <div style={{marginBottom: 4}}><b>Type:</b> {selectedNode.type}</div>
          {'ISIN' in selectedNode && (
            <>
              <div style={{marginBottom: 4}}><b>ISIN:</b> {selectedNode.ISIN}</div>
              <div style={{marginBottom: 4}}><b>시장:</b> {selectedNode.market}</div>
              <div style={{marginBottom: 4}}><b>통화:</b> {selectedNode.currency}</div>
              <div style={{marginBottom: 4}}><b>Price From:</b> {selectedNode.priceFrom}</div>
              <div style={{marginBottom: 4}}><b>Price To:</b> {selectedNode.priceTo}</div>
              <div style={{marginBottom: 4}}><b>Price Change:</b> {selectedNode.priceChange}</div>
            </>
          )}
          {'keyword' in selectedNode && (
            <>
              <div style={{marginBottom: 4}}><b>Keyword:</b> {selectedNode.keyword}</div>
              <div style={{marginBottom: 4}}><b>Price Change:</b> {selectedNode.priceChange}</div>
            </>
          )}
          <button style={{marginTop: 18, padding: '6px 16px', borderRadius: 8, border: '1px solid #334155', background: '#232b3a', color: '#7dd3fc', fontWeight: 500, cursor: 'pointer', transition: 'background 0.2s'}} onClick={() => setSelectedNode(null)} onMouseOver={e => (e.currentTarget.style.background='#334155')} onMouseOut={e => (e.currentTarget.style.background='#232b3a')}>닫기</button>
        </div>
      ) : null}
    </div>
  )
}

function GraphData() {
  const { data, isLoading, error } = useQuery<CompanyKeywordGraph>({
    queryKey: ['graphData'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/test')
      if (!res.ok) throw new Error('네트워크 오류')
      return res.json() as Promise<CompanyKeywordGraph>
    }
  })

  if (isLoading) return <div>로딩 중...</div>
  if (error) return <div>에러 발생: {(error as Error).message}</div>
  if (!data) return null

  return <D3Graph data={data} />
}

function App() {
  return (
    <>
      <GraphData />
    </>
  )
}

export default App

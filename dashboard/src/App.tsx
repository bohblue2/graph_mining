import { useQuery } from '@tanstack/react-query'
import { useEffect, useMemo, useRef, useState } from 'react'
import * as d3 from 'd3'
import { CompanyKeywordGraph, CompanyNode, KeywordNode } from './dto/graph';

// D3에서 사용할 수 있는 노드 타입 (id, name, x, y, fx, fy 포함)
type NodeType =
  (CompanyNode & { id: string; name: string; x?: number; y?: number; fx?: number|null; fy?: number|null }) |
  (KeywordNode & { id: string; name: string; x?: number; y?: number; fx?: number|null; fy?: number|null });

// D3에서 사용할 수 있는 링크 타입
type LinkType = { source: string; target: string; value: number; };

// source/target에서 id를 안전하게 추출하는 헬퍼
function getId(val: string | { id: string }): string {
  return typeof val === 'object' && val !== null ? val.id : val;
}

function D3Graph({ data }: { data: CompanyKeywordGraph }) {
  const svgRef = useRef<SVGSVGElement | null>(null)
  const [selectedNode, setSelectedNode] = useState<CompanyNode | KeywordNode | null>(null)

  // 물리 변수 상태
  const [chargeStrength, setChargeStrength] = useState(-150)
  const [linkDistance, setLinkDistance] = useState(60)
  const [linkStrength, setLinkStrength] = useState(0.5)
  const [gravityStrength, setGravityStrength] = useState(0.01)
  const [alphaDecay, setAlphaDecay] = useState(0.004)
  const [applyNegativeOnly, setApplyNegativeOnly] = useState(false)
  const simulationRef = useRef<d3.Simulation<NodeType, undefined> | null>(null)

  // 컨트롤 패널 숨기기/보이기 상태
  const [showControls, setShowControls] = useState(true);

  // D3에서 쓸 수 있도록 id, name, x, y, fx, fy만 추가
  const nodes: NodeType[] = useMemo(() => [
    ...data.company_nodes.map(n => ({ ...n, id: n.name, name: n.name })),
    ...data.keyword_nodes.map(n => ({ ...n, id: n.keyword, name: n.keyword }))
  ], [data.company_nodes, data.keyword_nodes]);
  
  // 항상 id(string) 기반으로 새로 만듦
  const links: LinkType[] = useMemo(() => 
    data.edges.map(e => ({ source: e.source, target: e.target, value: e.weight ?? 0 })),
    [data.edges]
  );
  
  // 토글에 따라 force에 쓸 링크만 필터링
  const filteredLinks = useMemo(() => 
    links.filter(link => applyNegativeOnly ? link.value < 0 : link.value > 0),
    [links, applyNegativeOnly]
  );

  // 슬라이더 값이 바뀔 때마다 force 파라미터를 실시간으로 갱신
  useEffect(() => {
    const simulation = simulationRef.current as unknown as d3.Simulation<NodeType, undefined>;
    if (!simulation) return;
    // charge
    const charge = simulation.force('charge') as d3.ForceManyBody<NodeType>;
    if (charge) charge.strength(chargeStrength);
    // link
    const linkForce = simulation.force('link') as d3.ForceLink<NodeType, LinkType>;
    if (linkForce) {
      linkForce.links(filteredLinks);
      linkForce.distance(linkDistance);
      linkForce.strength((link: LinkType) => Math.max(0, Math.min(1, Math.abs(link.value) * linkStrength)));
    }
    // gravity
    const gravityY = simulation.force('gravityY') as d3.ForceY<NodeType>;
    if (gravityY) gravityY.strength(gravityStrength);
    const gravityX = simulation.force('gravityX') as d3.ForceX<NodeType>;
    if (gravityX) gravityX.strength(gravityStrength);
    // alphaDecay
    simulation.alphaDecay(alphaDecay);
    // 부드럽게 재시작
    simulation.alpha(1).restart();
  }, [chargeStrength, linkDistance, linkStrength, gravityStrength, alphaDecay, applyNegativeOnly, filteredLinks]);

  useEffect(() => {
    if (!data) return

    // 기존 simulation 완전히 정지 및 해제
    if (simulationRef.current) {
      simulationRef.current.stop();
      simulationRef.current = null;
    }

    const width = window.innerWidth
    const height = window.innerHeight

    // D3 force simulation
    const manyBody = d3.forceManyBody().strength(chargeStrength);
    const simulation = d3.forceSimulation(nodes as d3.SimulationNodeDatum[])
      .force('link', d3.forceLink<NodeType, LinkType>(filteredLinks)
        .id((d: NodeType) => d.id)
        .distance(linkDistance)
        .strength((link: LinkType) => Math.max(0, Math.min(1, Math.abs(link.value) * linkStrength))))
      .force('charge', manyBody)
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('gravityY', d3.forceY(height / 2).strength(gravityStrength))
      .force('gravityX', d3.forceX(width / 2).strength(gravityStrength))
      .alpha(0.5)
      .alphaDecay(alphaDecay)

    simulationRef.current = simulation as unknown as d3.Simulation<NodeType, undefined>;

    // SVG 초기화
    const svg = d3.select(svgRef.current) as d3.Selection<SVGSVGElement, unknown, null, undefined>
    svg.selectAll('*').remove()

    // 줌/팬 그룹 생성
    const g = svg.append('g')

    // 링크
    const link = g.append('g')
      .selectAll('line')
      .data(
        filteredLinks,
        (d: unknown) => {
          const link = d as { source: string | { id: string }, target: string | { id: string } };
          return `${getId(link.source)}-${getId(link.target)}`;
        }
      )
      .enter()
      .append('line')
      .attr('stroke', (d: LinkType) => d.value < 0 ? '#ef4444' : '#7dd3fc')
      .attr('stroke-width', (d: LinkType) => 1 + Math.abs(d.value ?? 0) * 5)
      .attr('opacity', (d: LinkType) => {
        if (applyNegativeOnly) {
          return d.value < 0 ? 0.2 + Math.abs(d.value ?? 0) * 0.8 : 0.05;
        } else {
          return d.value > 0 ? 0.2 + Math.abs(d.value ?? 0) * 0.8 : 0.05;
        }
      })

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
          if (!event.active) simulation.alphaTarget(0.3).restart()
          d.fx = d.x
          d.fy = d.y
        })
        .on('drag', (event: d3.D3DragEvent<SVGGElement, NodeType, unknown>, d: NodeType) => {
          d.fx = event.x
          d.fy = event.y
        })
        .on('end', (event: d3.D3DragEvent<SVGGElement, NodeType, unknown>, d: NodeType) => {
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
        .scaleExtent([0.001, 1000])
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
      simulation.stop();
      simulationRef.current = null;
    }
  }, [data, applyNegativeOnly, links, chargeStrength, nodes, filteredLinks, linkDistance, gravityStrength, alphaDecay, linkStrength])

  return (
    <div className="flex justify-center items-center" style={{ width: '100vw', height: '100vh', background: '#181f2a' }}>
      {/* 컨트롤 패널 숨기기/보이기 */}
      {showControls ? (
        <div style={{
          position: 'fixed',
          top: 32,
          left: 32,
          background: 'linear-gradient(135deg, #232a36 80%, #1a202c 100%)',
          border: '1.5px solid #293040',
          borderRadius: 18,
          boxShadow: '0 8px 32px 0 rgba(0,0,0,0.28)',
          padding: 28,
          zIndex: 2000,
          color: '#e5e7eb',
          minWidth: 300,
          maxWidth: 340,
          fontFamily: 'Inter, Pretendard, sans-serif',
          fontSize: 15,
          letterSpacing: 0.01,
          backdropFilter: 'blur(10px)',
          transition: 'box-shadow 0.2s',
        }}>
          {/* 숨기기 버튼 */}
          <button onClick={() => setShowControls(false)} style={{
            position: 'absolute',
            top: 12,
            right: 12,
            background: 'none',
            border: 'none',
            color: '#7dd3fc',
            fontSize: 22,
            cursor: 'pointer',
            padding: 0,
            opacity: 0.7,
            transition: 'opacity 0.2s',
          }} title="숨기기">✕</button>
          <div style={{fontWeight: 700, marginBottom: 16, color: '#60a5fa', fontSize: 20, letterSpacing: 0.5}}>Physics Controls</div>
          <div style={{marginBottom: 16}}>
            <label style={{display: 'block', marginBottom: 4, color: '#a5b4fc', fontWeight: 500}}>반발력(charge): <span style={{color:'#60a5fa'}}>{chargeStrength}</span></label>
            <input type="range" min="-500" max="0" step="1" value={chargeStrength} onChange={e => setChargeStrength(Number(e.target.value))} style={{width: '100%', accentColor:'#60a5fa', height: 4, borderRadius: 4}} />
          </div>
          <div style={{marginBottom: 16}}>
            <label style={{display: 'block', marginBottom: 4, color: '#a5b4fc', fontWeight: 500}}>링크 거리: <span style={{color:'#60a5fa'}}>{linkDistance}</span></label>
            <input type="range" min="10" max="200" step="1" value={linkDistance} onChange={e => setLinkDistance(Number(e.target.value))} style={{width: '100%', accentColor:'#60a5fa', height: 4, borderRadius: 4}} />
          </div>
          <div style={{marginBottom: 16}}>
            <label style={{display: 'block', marginBottom: 4, color: '#a5b4fc', fontWeight: 500}}>링크 강도: <span style={{color:'#60a5fa'}}>{linkStrength}</span></label>
            <input type="range" min="0" max="2" step="0.01" value={linkStrength} onChange={e => setLinkStrength(Number(e.target.value))} style={{width: '100%', accentColor:'#60a5fa', height: 4, borderRadius: 4}} />
          </div>
          <div style={{marginBottom: 16}}>
            <label style={{display: 'block', marginBottom: 4, color: '#a5b4fc', fontWeight: 500}}>중력(gravity): <span style={{color:'#60a5fa'}}>{gravityStrength}</span></label>
            <input type="range" min="0" max="0.5" step="0.01" value={gravityStrength} onChange={e => setGravityStrength(Number(e.target.value))} style={{width: '100%', accentColor:'#60a5fa', height: 4, borderRadius: 4}} />
          </div>
          <div style={{marginBottom: 16}}>
            <label style={{display: 'block', marginBottom: 4, color: '#a5b4fc', fontWeight: 500}}>alphaDecay: <span style={{color:'#60a5fa'}}>{alphaDecay}</span></label>
            <input type="range" min="0.0" max="0.2" step="0.001" value={alphaDecay} onChange={e => setAlphaDecay(Number(e.target.value))} style={{width: '100%', accentColor:'#60a5fa', height: 4, borderRadius: 4}} />
          </div>
          <div style={{marginBottom: 0, display: 'flex', alignItems: 'center', gap: 10}}>
            <label style={{color: '#a5b4fc', fontWeight: 500, flex: 1}}>음수 링크 적용</label>
            <label style={{display: 'flex', alignItems: 'center', gap: 6, cursor: 'pointer'}}>
              <input type="checkbox" checked={applyNegativeOnly} onChange={e => setApplyNegativeOnly(e.target.checked)} style={{width: 18, height: 18, accentColor:'#60a5fa', cursor: 'pointer', borderRadius: 6, boxShadow: '0 1px 2px #0002'}} />
              <span style={{color: applyNegativeOnly ? '#60a5fa' : '#a5b4fc', fontWeight: 600, fontSize: 15}}>{applyNegativeOnly ? '음수' : '양수'}</span>
            </label>
          </div>
        </div>
      ) : (
        <button
          onClick={() => setShowControls(true)}
          style={{
            position: 'fixed',
            top: 32,
            left: 32,
            width: 48,
            height: 48,
            padding: 0,
            borderRadius: '20%',
            background: '#232a36',
            border: '1.5px solid #293040',
            boxShadow: '0 4px 16px 0 rgba(0,0,0,0.18)',
            color: '#60a5fa',
            fontSize: 28,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            zIndex: 2000,
            transition: 'box-shadow 0.2s',
          }}
          title="Physics Controls 열기"
        >
          <span role="img" aria-label="설정">⚙</span>
        </button>
      )}
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

import { TraversalInterface } from '../components/TraversalInterface';

export default function HomePage() {
  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">Chirality Framework</h1>
      <p className="text-gray-600 mb-8">11-Station Semantic Valley Traversal</p>
      
      <TraversalInterface />
    </div>
  );
}
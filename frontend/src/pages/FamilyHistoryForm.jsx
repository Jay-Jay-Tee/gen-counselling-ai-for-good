import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, Plus, X, Loader, AlertCircle } from 'lucide-react';

function FamilyHistoryForm({ formData, updateFormData, onNext, onBack }) {
  const navigate = useNavigate();
  const [diseases, setDiseases] = useState([]);
  const [loadingDiseases, setLoadingDiseases] = useState(true);
  const [diseaseError, setDiseaseError] = useState(null);
  
  // Initialize with parents and grandparents
  const [familyMembers, setFamilyMembers] = useState(
    formData.family.length > 0 ? formData.family : [
      { role: 'mother', generation: 1, known_issues: [] },
      { role: 'father', generation: 1, known_issues: [] },
      { role: 'maternal_grandmother', generation: 2, known_issues: [] },
      { role: 'maternal_grandfather', generation: 2, known_issues: [] },
      { role: 'paternal_grandmother', generation: 2, known_issues: [] },
      { role: 'paternal_grandfather', generation: 2, known_issues: [] }
    ]
  );

  // Fetch diseases from backend
  useEffect(() => {
    const fetchDiseases = async () => {
      try {
        setLoadingDiseases(true);
        const response = await fetch('/api/disease-info');
        
        if (!response.ok) {
          throw new Error('Failed to fetch diseases');
        }
        
        const data = await response.json();
        // Expecting: { diseases: [{ id: "type2_diabetes", name: "Type 2 Diabetes" }] }
        setDiseases(data.diseases || []);
        setDiseaseError(null);
      } catch (error) {
        console.error('Error fetching diseases:', error);
        setDiseaseError(error.message);
        // Fallback to empty array if fetch fails
        setDiseases([]);
      } finally {
        setLoadingDiseases(false);
      }
    };

    fetchDiseases();
  }, []);

  const addFamilyMember = (role, generation) => {
    const newMember = {
      role,
      generation,
      known_issues: [],
      id: Date.now() // Unique ID for dynamic members
    };
    setFamilyMembers([...familyMembers, newMember]);
  };

  const removeFamilyMember = (index) => {
    setFamilyMembers(familyMembers.filter((_, i) => i !== index));
  };

  const toggleDisease = (memberIndex, diseaseId) => {
    const updated = [...familyMembers];
    const member = updated[memberIndex];
    
    if (member.known_issues.includes(diseaseId)) {
      // Remove disease
      member.known_issues = member.known_issues.filter(id => id !== diseaseId);
    } else {
      // Add disease
      member.known_issues = [...member.known_issues, diseaseId];
    }
    
    setFamilyMembers(updated);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Clean up family data - remove members with no diseases
    const cleanedFamily = familyMembers
      .filter(member => member.known_issues.length > 0)
      .map(member => {
        // Remove temporary id field
        const { id, ...memberData } = member;
        return memberData;
      });
    
    updateFormData('family', cleanedFamily);
    if (onNext) {
      onNext();
    } else {
      navigate('/upload-report');
    }
  };

  const getFamilyMemberLabel = (role) => {
    return role.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  const renderFamilyMember = (member, index) => {
    const isFixed = ['mother', 'father', 'maternal_grandmother', 'maternal_grandfather', 
                     'paternal_grandmother', 'paternal_grandfather'].includes(member.role);

    return (
      <div key={index} className="bg-gray-50 rounded-lg p-4 mb-4">
        <div className="flex justify-between items-center mb-3">
          <h4 className="font-semibold text-gray-800">
            {getFamilyMemberLabel(member.role)}
          </h4>
          {!isFixed && (
            <button
              type="button"
              onClick={() => removeFamilyMember(index)}
              className="text-red-600 hover:text-red-700"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {diseases.map(disease => (
            <label key={disease.id} className="flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={member.known_issues.includes(disease.id)}
                onChange={() => toggleDisease(index, disease.id)}
                className="w-4 h-4 text-indigo-600 focus:ring-indigo-500 rounded"
              />
              <span className="ml-2 text-sm text-gray-700">
                {disease.name}
              </span>
            </label>
          ))}
        </div>
      </div>
    );
  };

  const generation1 = familyMembers.filter(m => m.generation === 1);
  const generation0 = familyMembers.filter(m => m.generation === 0);
  const generationNeg1 = familyMembers.filter(m => m.generation === -1);
  const generation2 = familyMembers.filter(m => m.generation === 2);

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between mb-2">
            <span className="text-sm font-medium text-indigo-600">Step 3 of 4</span>
            <span className="text-sm text-gray-500">Family History</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-indigo-600 h-2 rounded-full" style={{ width: '75%' }}></div>
          </div>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="flex items-center mb-6">
            <Users className="w-8 h-8 text-indigo-600 mr-3" />
            <h2 className="text-2xl font-bold text-gray-900">Family Medical History</h2>
          </div>

          <p className="text-gray-600 mb-6">
            Check any conditions that your family members have been diagnosed with. Leave unchecked if they don't have any conditions.
          </p>

          {/* Loading State */}
          {loadingDiseases && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6 text-center">
              <Loader className="w-8 h-8 text-blue-600 animate-spin mx-auto mb-2" />
              <p className="text-blue-700">Loading disease information...</p>
            </div>
          )}

          {/* Error State */}
          {diseaseError && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-6 mb-6">
              <div className="flex items-start">
                <AlertCircle className="w-6 h-6 text-red-600 mr-3 mt-0.5" />
                <div>
                  <h3 className="font-semibold text-red-800 mb-1">Failed to Load Diseases</h3>
                  <p className="text-red-700 text-sm">{diseaseError}</p>
                  <button
                    type="button"
                    onClick={() => window.location.reload()}
                    className="mt-3 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm"
                  >
                    Retry
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* No Diseases Warning */}
          {!loadingDiseases && !diseaseError && diseases.length === 0 && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-6">
              <div className="flex items-start">
                <AlertCircle className="w-6 h-6 text-yellow-600 mr-3 mt-0.5" />
                <div>
                  <h3 className="font-semibold text-yellow-800 mb-1">No Diseases Available</h3>
                  <p className="text-yellow-700 text-sm">
                    Unable to load disease list. Please contact support or try again later.
                  </p>
                </div>
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Generation 1: Parents */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">
                Generation 1: Parents
              </h3>
              {generation1.map((member, idx) => 
                renderFamilyMember(member, familyMembers.indexOf(member))
              )}
            </div>

            {/* Generation 0: Siblings */}
            <div>
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-gray-800">
                  Generation 0: Siblings (Optional)
                </h3>
                <div className="flex space-x-2">
                  <button
                    type="button"
                    onClick={() => addFamilyMember('brother', 0)}
                    className="flex items-center px-3 py-1 text-sm bg-indigo-100 text-indigo-700 rounded-lg hover:bg-indigo-200"
                  >
                    <Plus className="w-4 h-4 mr-1" />
                    Add Brother
                  </button>
                  <button
                    type="button"
                    onClick={() => addFamilyMember('sister', 0)}
                    className="flex items-center px-3 py-1 text-sm bg-indigo-100 text-indigo-700 rounded-lg hover:bg-indigo-200"
                  >
                    <Plus className="w-4 h-4 mr-1" />
                    Add Sister
                  </button>
                </div>
              </div>
              {generation0.length === 0 ? (
                <p className="text-gray-500 text-sm italic">No siblings added</p>
              ) : (
                generation0.map((member, idx) => 
                  renderFamilyMember(member, familyMembers.indexOf(member))
                )
              )}
            </div>

            {/* Generation -1: Children */}
            <div>
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-gray-800">
                  Generation -1: Children (Optional)
                </h3>
                <div className="flex space-x-2">
                  <button
                    type="button"
                    onClick={() => addFamilyMember('son', -1)}
                    className="flex items-center px-3 py-1 text-sm bg-indigo-100 text-indigo-700 rounded-lg hover:bg-indigo-200"
                  >
                    <Plus className="w-4 h-4 mr-1" />
                    Add Son
                  </button>
                  <button
                    type="button"
                    onClick={() => addFamilyMember('daughter', -1)}
                    className="flex items-center px-3 py-1 text-sm bg-indigo-100 text-indigo-700 rounded-lg hover:bg-indigo-200"
                  >
                    <Plus className="w-4 h-4 mr-1" />
                    Add Daughter
                  </button>
                </div>
              </div>
              {generationNeg1.length === 0 ? (
                <p className="text-gray-500 text-sm italic">No children added</p>
              ) : (
                generationNeg1.map((member, idx) => 
                  renderFamilyMember(member, familyMembers.indexOf(member))
                )
              )}
            </div>

            {/* Generation 2: Extended Family */}
            <div>
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-gray-800">
                  Generation 2: Grandparents & Extended Family
                </h3>
                <div className="flex flex-wrap gap-2">
                  <button
                    type="button"
                    onClick={() => addFamilyMember('maternal_aunt', 2)}
                    className="flex items-center px-3 py-1 text-sm bg-indigo-100 text-indigo-700 rounded-lg hover:bg-indigo-200"
                  >
                    <Plus className="w-4 h-4 mr-1" />
                    Maternal Aunt
                  </button>
                  <button
                    type="button"
                    onClick={() => addFamilyMember('maternal_uncle', 2)}
                    className="flex items-center px-3 py-1 text-sm bg-indigo-100 text-indigo-700 rounded-lg hover:bg-indigo-200"
                  >
                    <Plus className="w-4 h-4 mr-1" />
                    Maternal Uncle
                  </button>
                  <button
                    type="button"
                    onClick={() => addFamilyMember('paternal_aunt', 2)}
                    className="flex items-center px-3 py-1 text-sm bg-indigo-100 text-indigo-700 rounded-lg hover:bg-indigo-200"
                  >
                    <Plus className="w-4 h-4 mr-1" />
                    Paternal Aunt
                  </button>
                  <button
                    type="button"
                    onClick={() => addFamilyMember('paternal_uncle', 2)}
                    className="flex items-center px-3 py-1 text-sm bg-indigo-100 text-indigo-700 rounded-lg hover:bg-indigo-200"
                  >
                    <Plus className="w-4 h-4 mr-1" />
                    Paternal Uncle
                  </button>
                </div>
              </div>
              {generation2.map((member, idx) => 
                renderFamilyMember(member, familyMembers.indexOf(member))
              )}
            </div>

            {/* Submit Buttons */}
            <div className="flex justify-between pt-6">
              <button
                type="button"
                onClick={() => onBack ? onBack() : navigate('/lifestyle')}
                className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
              >
                Back
              </button>
              <button
                type="submit"
                disabled={loadingDiseases || diseaseError}
                className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default FamilyHistoryForm;

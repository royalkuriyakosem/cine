import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Spinner } from '../../components/ui/Spinner';
import { Button } from '../../components/ui/Button';
import { Modal } from '../../components/ui/Modal';
import { FileUpload } from '../../components/ui/FileUpload';
import { getVFXShots, getShotVersions, uploadVFXVersion } from '../../api/vfx';

const VFXBoard = ({ productionId }) => {
    const [shots, setShots] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');
    const [selectedShot, setSelectedShot] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [versions, setVersions] = useState([]);
    const [isUploading, setIsUploading] = useState(false);

    useEffect(() => {
        const fetchShots = async () => {
            if (!productionId) return;
            try {
                setIsLoading(true);
                const data = await getVFXShots(productionId);
                setShots(data);
            } catch (err) {
                setError('Failed to load VFX shots.');
            } finally {
                setIsLoading(false);
            }
        };
        fetchShots();
    }, [productionId]);

    const handleViewVersions = async (shot) => {
        setSelectedShot(shot);
        setIsModalOpen(true);
        try {
            const versionData = await getShotVersions(shot.id);
            setVersions(versionData);
        } catch (err) {
            setError('Failed to load versions.');
        }
    };

    const handleUpload = async (file, notes) => {
        if (!file || !selectedShot) return;
        setIsUploading(true);
        try {
            await uploadVFXVersion(selectedShot.id, file, notes);
            // Refresh versions
            const versionData = await getShotVersions(selectedShot.id);
            setVersions(versionData);
        } catch (err) {
            setError('Upload failed.');
        } finally {
            setIsUploading(false);
        }
    };

    const UploadModalContent = () => {
        const [file, setFile] = useState(null);
        const [notes, setNotes] = useState('');
        return (
            <div className="space-y-4">
                <h4 className="font-bold">Upload New Version for Shot {selectedShot?.shot}</h4>
                <FileUpload onFileSelect={setFile} />
                <textarea
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    placeholder="Version notes..."
                    className="w-full p-2 border rounded"
                />
                <Button onClick={() => handleUpload(file, notes)} disabled={isUploading}>
                    {isUploading ? <Spinner /> : 'Upload'}
                </Button>
            </div>
        );
    };

    if (isLoading) return <Spinner />;
    if (error) return <p className="text-red-500">{error}</p>;

    return (
        <Card>
            <h3 className="text-xl font-bold mb-4 text-gray-800">VFX Board</h3>
            <div className="overflow-x-auto">
                <table className="min-w-full bg-white border">
                    <thead className="bg-gray-200">
                        <tr>
                            <th className="py-2 px-4 border-b">Scene/Shot</th>
                            <th className="py-2 px-4 border-b">Status</th>
                            <th className="py-2 px-4 border-b">Assigned Team</th>
                            <th className="py-2 px-4 border-b">Due Date</th>
                            <th className="py-2 px-4 border-b">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {shots.map(shot => (
                            <tr key={shot.id}>
                                <td className="py-2 px-4 border-b">Scene {shot.scene} / Shot {shot.shot}</td>
                                <td className="py-2 px-4 border-b">{shot.status}</td>
                                <td className="py-2 px-4 border-b">{shot.assigned_team || 'N/A'}</td>
                                <td className="py-2 px-4 border-b">{shot.due_date || 'N/A'}</td>
                                <td className="py-2 px-4 border-b space-x-2">
                                    <Button onClick={() => handleViewVersions(shot)} size="sm">Versions</Button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
                {selectedShot && (
                    <div>
                        <h3 className="text-lg font-bold mb-4">Version History for Shot {selectedShot.shot}</h3>
                        <div className="mb-6 p-4 border rounded bg-gray-50">
                           <UploadModalContent />
                        </div>
                        <ul className="space-y-2">
                            {versions.map(v => (
                                <li key={v.id} className="p-2 border rounded">
                                    Version {v.version_number} - {v.notes || 'No notes'} ({new Date(v.uploaded_at).toLocaleDateString()})
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </Modal>
        </Card>
    );
};

export default VFXBoard;
import { useState } from "react";
import { Upload } from "lucide-react";

function ResumeUpload() {
    const [resumeFile, setResumeFile] = useState(null);
    const [jobInput, setJobInput] = useState('');
    const [submissionFlag, setSubmissionFlag] = useState(false);
    const [resultData, setResultData] = useState(null);

    const handleFileChange = (event) => {
        setResumeFile(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!resumeFile || !jobInput) {
            alert("Please upload a resume and enter a job link!");
            return;
        }

        const formData = new FormData();
        formData.append('resume', resumeFile);
        formData.append('job', jobInput);

        try {
            const response = await fetch("http://localhost:8000/match_requirements", {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                setResultData(result); 
                setSubmissionFlag(true); 
            } else {
                alert("Failed to upload file and data.");
            }
        } catch (error) {
            console.error("Error uploading file and data: ", error);
        }
    };

    return (
        <div className="max-w-md mx-auto py-10 px-12 border rounded-lg shadow-lg bg-gray-900 text-white">
            {/* Show form only if submission has NOT happened */}
            {!submissionFlag ? (
                <form className="flex flex-col gap-6" onSubmit={handleSubmit}>
                    {/* Resume Upload */}
                    <div>
                        <label htmlFor="resume" className="text-lg font-bold flex items-center gap-2">
                            <Upload size={20} /> Upload your resume:
                        </label>
                        <input
                            type="file"
                            id="resume"
                            accept=".pdf,.docx"
                            className="border p-3 rounded-lg w-full mt-2 bg-gray-800"
                            onChange={handleFileChange}
                            required
                        />
                        {resumeFile && <p className="text-sm text-gray-400 mt-1">Selected: {resumeFile.name}</p>}
                    </div>

                    {/* Job Posting Input */}
                    <div>
                        <label htmlFor="job" className="text-lg font-bold flex items-center gap-2">
                            <Upload size={20} /> Link a job posting (LinkedIn):
                        </label>
                        <input
                            type="text"
                            id="job"
                            value={jobInput}
                            onChange={(e) => setJobInput(e.target.value)}
                            placeholder="https://www.linkedin.com/jobs/view/1234567890"
                            className="border p-2 rounded-lg w-full mt-2 bg-gray-800"
                            required
                        />
                    </div>

                    {/* Submit Button */}
                    <button type="submit" className="border py-2.5 rounded-lg">
                        Upload Files
                    </button>
                </form>
            ) : (
                <div>
                    {/* Display Submission Results */}
                    <h2 className="text-xl font-bold text-green-400">Submission Successful!</h2>
                    {resultData ? (
                        <div className="mt-4 p-6 border rounded-lg bg-gray-800 flex-col">
                            <div className="flex justify-between mb-2">
                                <strong className="text-left">Job Title:</strong>
                                <span className="text-center flex-1">{resultData.job_title}</span>
                            </div>
                            <div className="flex justify-between mb-2">
                                <strong className="text-left">Company:</strong>
                                <span className="text-center flex-1">{resultData.company}</span>
                            </div>
                            <div className="flex justify-between mb-2">
                                <strong className="text-left">Description:</strong>
                                <span className="text-center flex-1">{resultData.description}</span>
                            </div>
                        </div>
                    ) : (
                        <p className="text-gray-400">Processing your data...</p>
                    )}
                </div>
            )}
        </div>
    );
}

export default ResumeUpload;

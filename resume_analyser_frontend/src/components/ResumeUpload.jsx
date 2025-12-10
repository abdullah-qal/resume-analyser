import { useEffect, useState } from "react";
import { Upload } from "lucide-react";

function ResumeUpload() {
    const [resumeFile, setResumeFile] = useState(null);
    const [jobInput, setJobInput] = useState('');
    const [submissionFlag, setSubmissionFlag] = useState(false);
    const [resultData, setResultData] = useState(null);
    const [csrfToken, setCsrfToken] = useState('');
    const [error, setError] = useState('');

    const handleFileChange = (event) => {
        setResumeFile(event.target.files[0]);
    };

    useEffect(() => {
        const fetchCsrf = async () => {
            try {
                await fetch("http://localhost:8000/csrf/", {
                    credentials: "include",
                });
                const token = document.cookie
                    .split("; ")
                    .find((row) => row.startsWith("csrftoken="))
                    ?.split("=")[1];
                if (token) {
                    setCsrfToken(token);
                }
            } catch (err) {
                console.error("Unable to fetch CSRF token", err);
            }
        };
        fetchCsrf();
    }, []);

    const handleSubmit = async (event) => {
        event.preventDefault();

        setError('');

        if (!resumeFile || !jobInput) {
            alert("Please upload a resume and enter a job link!");
            return;
        }

        if (!csrfToken) {
            alert("Unable to submit without CSRF token. Please refresh and try again.");
            return;
        }

        const formData = new FormData();
        formData.append('resume', resumeFile);
        formData.append('job', jobInput);

        try {
            const response = await fetch("http://localhost:8000/match_requirements", {
                method: 'POST',
                credentials: "include",
                headers: {
                    "X-CSRFToken": csrfToken,
                },
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                setResultData(result); 
                setSubmissionFlag(true); 
            } else {
                const payload = await response.json().catch(() => ({}));
                setError(payload.error || "Failed to upload file and data.");
            }
        } catch (error) {
            console.error("Error uploading file and data: ", error);
            setError("Unexpected error uploading file.");
        }
    };

    return (
        <div className="max-w-md mx-auto py-10 px-12 border rounded-lg shadow-lg bg-gray-900 text-white">
            {/* Show form only if submission has NOT happened */}
            {!submissionFlag ? (
                <form className="flex flex-col gap-6" onSubmit={handleSubmit}>
                    {error && <p className="text-red-400 text-sm">{error}</p>}
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
                                <span className="text-center flex-1 text-left">{resultData.description}</span>
                            </div>
                            <div className="flex justify-between mb-2">
                                <strong className="text-left">Match score:</strong>
                                <span className="text-center flex-1">{resultData.match_score}%</span>
                            </div>
                            {resultData.matched_terms?.length ? (
                                <div className="mt-2 text-left">
                                    <strong>Key terms matched:</strong>
                                    <p className="text-sm text-gray-300 mt-1">
                                        {resultData.matched_terms.join(', ')}
                                    </p>
                                </div>
                            ) : null}
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

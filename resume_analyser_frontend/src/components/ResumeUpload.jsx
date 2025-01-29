function ResumeUpload() {
    return (
    <form className="flex flex-col gap-6 p-10 border rounded-lg shadow-lg">
        <label 
            htmlFor="resume" 
            className="text-lg font-bold"
        > 
            Upload your resume:
        </label>
        <input
            type="file"
            name="resume"
            id="resume"
            accept=".pdf,.docx"
            className="w-full border p-3 rounded-lg"
            required
        />
        <button
            type="submit"
            className="bg-blue-500 text-white w-full rounded-lg hover:bg-blue-600 transition border"
        >
            Upload
        </button>
    </form>
    )
}
export default ResumeUpload;

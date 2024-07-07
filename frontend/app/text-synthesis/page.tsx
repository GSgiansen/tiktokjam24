"use client";

import { useEffect, useRef, useState } from "react";
import { createClient } from "@/utils/supabase/client";
import { useRouter } from "next/navigation";
import Image from "next/image";

const UploadPage = () => {
    const supabase = createClient();
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [uploadedFile, setUploadedFile] = useState(null);
    const inputRef = useRef("");
    const iterCountRef = useRef(0);
    const [authenticated, setAuthenticated] = useState(false);
    const [accessToken, setAccessToken] = useState<string>("");

    useEffect(() => {
        const checkSession = async () => {
            const {
                data: { session },
            } = await supabase.auth.getSession();
            if (!session) {
                router.push("/login");
            } else {
                setAccessToken(session.access_token);
                setAuthenticated(true);
            }
        };
        checkSession();
    }, []);

    const handleSubmit = async (event) => {
        event.preventDefault();

        setLoading(true);

        const formData = new FormData();
        formData.append("file", uploadedFile);
        formData.append("input", inputRef.current.value)
        formData.append("iter_count", iterCountRef.current.value)

        console.log(formData);

        try {
            const response = await fetch("http://128.199.130.222:8000/synthesize_data", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                },
                body: formData,
            });

            await response.blob()
                .then((blob) => {
                    let file = window.URL.createObjectURL(blob);
                    window.location.assign(file);
                })
        } catch (error) {
            console.error(error);
        }

        setLoading(false)
    };

    const handleFileChange = (event) => {
        setLoading(true);
        setUploadedFile(event.target.files[0]);
        setLoading(false);
    };

    const showFileUploadState = () => {
        if (loading) {
            return (
                <div
                    className="flex justify-center items-center min-h-screen"
                    role="status"
                >
                    <svg
                        aria-hidden="true"
                        className="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                        viewBox="0 0 100 101"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                            fill="currentColor"
                        />
                        <path
                            d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                            fill="currentFill"
                        />
                    </svg>
                </div>
            );
        }
        if (uploadedFile) {
            return (
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                    <Image
                        className="w-8 h-8 mb-5"
                        src="/icons/tick-circle-svgrepo-com.svg"
                        alt=""
                        width={24}
                        height={24}
                    />
                    <p className="mb-2 text-sm text-white 0">
                        <span className="font-semibold">File uploaded successfully:</span>{" "}
                        {uploadedFile.name}
                    </p>
                    <p className="mb-2 text-sm text-white">
                        Click or drag and drop again to re-upload
                    </p>
                </div>
            );
        } else {
            return (
                <div className="flex justify-center items-center min-h-screen">
                    <div className="flex flex-col items-center justify-center pt-5 pb-6">
                        <svg
                            className="w-8 h-8 mb-4 text-gray-500 "
                            aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 20 16"
                        >
                            <path
                                stroke="currentColor"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth="2"
                                d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
                            />
                        </svg>
                        <p className="mb-2 text-sm text-white">
                            <span className="font-semibold">Click to upload</span> or drag and
                            drop
                        </p>
                        <p className="text-xs text-white">
                            Supported extensions: .CSV
                        </p>
                    </div>
                </div>
            );
        }
    };


    return (
        <div className="p-6 mt-10">
            <form
                className="bg-slate-800 text-white shadow-md rounded px-8 pt-6 pb-6 mb-4"
                onSubmit={handleSubmit}
            >
                <label
                    className="block text-md font-bold mb-2"
                    htmlFor="Source"
                >
                    Upload a file for text synthesis
                </label>
                <div className="flex items-center justify-center w-full mt-3 mb-4" >
                    <label
                        htmlFor="dropzone-file"
                        className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-500 border-dashed rounded-lg cursor-pointer bg-slate-700 hover:bg-slate-600"
                    >
                        {showFileUploadState()}
                        <input
                            id="dropzone-file"
                            type="file"
                            className="hidden"
                            onChange={handleFileChange}
                            disabled={loading}
                        />
                    </label>
                </div>
                <div>
                    <div className="flex justify-center">
                        <label htmlFor="input" className="block p-2 text-sm font-medium text-gray-900 dark:text-white">Do you have any specific requirements for the augmented data?</label>
                        <input type="text" id="input" ref={inputRef} className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required />
                    </div>
                    <div className="flex justify-center">
                        <label htmlFor="iter_count" className="block p-2 text-sm font-medium text-gray-900 dark:text-white">How many new rows would you like to generate? (MAX 200)</label>
                        <input type="number" id="iter_count" ref={iterCountRef}className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required />
                    </div>
                </div>
                <div className="flex justify-center">
                    <button
                        className="bg-gray-900 w-48 hover:bg-gray-700 text-white py-2 px-4 rounded focus:outline-none focus:shadow-outline  disabled:bg-slate-600 disabled:text-slate-200 disabled:border-slate-500 disabled:shadow-none"
                        type="submit"
                        disabled={loading}
                    >
                        Submit
                    </button>
                </div>
            </form>
        </div>
    );

};

export default UploadPage;

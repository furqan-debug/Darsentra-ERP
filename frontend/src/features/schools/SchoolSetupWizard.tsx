import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  Building,
  CheckCircle,
  GraduationCap,
  MapPin,
  Rocket,
  School as SchoolIcon,
  Sparkles,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/context/AuthContext";
import authService from "@/services/authService";

const CURRICULUM_OPTIONS = [
  {
    id: "matric_fsc",
    label: "Matric / FSc (BISE)",
    description: "Standard Pakistani Board Curriculum (Science, Arts, Pre-Medical, Pre-Engineering)",
    defaultClasses: ["Nursery", "Prep", "Class 1", "Class 2", "Class 3", "Class 4", "Class 5", "Class 6", "Class 7", "Class 8", "Class 9", "Class 10"],
  },
  {
    id: "cambridge",
    label: "Cambridge (O / A Levels)",
    description: "British International curriculum (Checkpoint, IGCSE/O-Levels, AS & A-Levels)",
    defaultClasses: ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Grade 7", "Grade 8", "O-1", "O-2", "O-3", "A-1", "A-2"],
  },
  {
    id: "federal_board",
    label: "Federal Board (FBISE)",
    description: "Curriculum tailored for Islamabad Capital Territory and Federal institutions",
    defaultClasses: ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5", "Class 6", "Class 7", "Class 8", "Class 9", "Class 10"],
  },
  {
    id: "combined",
    label: "Combined / Dual Stream",
    description: "Dual system supporting both National Board and International streams simultaneously",
    defaultClasses: ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5", "Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "O-Levels", "A-Levels"],
  },
];

const PROVINCE_OPTIONS = [
  { id: "islamabad", label: "Islamabad Capital Territory" },
  { id: "punjab", label: "Punjab" },
  { id: "sindh", label: "Sindh" },
  { id: "kpk", label: "Khyber Pakhtunkhwa" },
  { id: "balochistan", label: "Balochistan" },
  { id: "ajk", label: "Azad Jammu & Kashmir" },
  { id: "gilgit_baltistan", label: "Gilgit-Baltistan" },
];

export const SchoolSetupWizard: React.FC = () => {
  const { user, refreshActiveSchool } = useAuth();
  const navigate = useNavigate();

  const [step, setStep] = useState<1 | 2 | 3>(1);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Form State
  const [name, setName] = useState("");
  const [code, setCode] = useState("");
  const [registrationNumber, setRegistrationNumber] = useState("");
  const [contactEmail, setContactEmail] = useState(user?.email || "");
  const [phoneNumber, setPhoneNumber] = useState(user?.phone_number || "");
  const [curriculumType, setCurriculumType] = useState("matric_fsc");
  const [province, setProvince] = useState("punjab");
  const [city, setCity] = useState("Lahore");
  const [address, setAddress] = useState("");
  const [academicYearName, setAcademicYearName] = useState("2026-2027");
  const [selectedClasses, setSelectedClasses] = useState<string[]>(
    CURRICULUM_OPTIONS[0].defaultClasses
  );

  const handleCurriculumSelect = (currId: string) => {
    setCurriculumType(currId);
    const curr = CURRICULUM_OPTIONS.find((c) => c.id === currId);
    if (curr) {
      setSelectedClasses(curr.defaultClasses);
    }
  };

  const handleToggleClass = (className: string) => {
    if (selectedClasses.includes(className)) {
      setSelectedClasses(selectedClasses.filter((c) => c !== className));
    } else {
      setSelectedClasses([...selectedClasses, className]);
    }
  };

  const handleNext = () => {
    setErrorMessage(null);
    if (step === 1) {
      if (!name.trim()) {
        setErrorMessage("Please enter the school institution name.");
        return;
      }
      if (!code.trim()) {
        setErrorMessage("Please enter an institutional campus code (e.g. KIPS-01).");
        return;
      }
      setStep(2);
    } else if (step === 2) {
      if (!city.trim()) {
        setErrorMessage("Please provide the campus city.");
        return;
      }
      setStep(3);
    }
  };

  const handlePrev = () => {
    setErrorMessage(null);
    if (step > 1) {
      setStep((step - 1) as 1 | 2);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    if (selectedClasses.length === 0) {
      setErrorMessage("Please select at least one class grade to initialize.");
      return;
    }

    setIsLoading(true);

    try {
      await authService.setupSchool({
        name,
        code,
        registration_number: registrationNumber,
        curriculum_type: curriculumType,
        contact_email: contactEmail,
        phone_number: phoneNumber,
        province,
        city,
        address,
        academic_year_name: academicYearName,
        initial_classes: selectedClasses,
      });

      await refreshActiveSchool();
      navigate("/dashboard", { replace: true });
    } catch (err: any) {
      if (err?.errors) {
        const errorKey = Object.keys(err.errors)[0];
        const msg = Array.isArray(err.errors[errorKey]) ? err.errors[errorKey][0] : err.errors[errorKey];
        setErrorMessage(`${errorKey}: ${msg}`);
      } else if (err?.message) {
        setErrorMessage(err.message);
      } else {
        setErrorMessage("Setup failed. Please check the institutional code for duplicates.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-6 px-4">
      {/* Wizard Header */}
      <div className="text-center space-y-2 mb-8">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-teal-50 dark:bg-teal-950/60 border border-teal-200 dark:border-teal-800 text-teal-800 dark:text-teal-300 text-xs font-medium">
          <Sparkles className="h-3.5 w-3.5 text-teal-600" />
          <span>Tenant Initialization Wizard</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">
          Set Up Your School Institution
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Welcome, {user?.first_name || "Founder"}. Complete this 3-step setup to launch your dedicated school tenant.
        </p>
      </div>

      {/* Steps Indicator */}
      <div className="grid grid-cols-3 gap-2 sm:gap-4 mb-8">
        <div
          className={`flex items-center space-x-2 p-2.5 sm:p-3 rounded-lg border transition-all ${
            step === 1
              ? "border-teal-600 bg-teal-50/50 dark:bg-teal-950/40 text-teal-900 dark:text-teal-200 shadow-sm"
              : step > 1
              ? "border-emerald-300 bg-emerald-50/30 text-emerald-800 dark:border-emerald-800 dark:text-emerald-300"
              : "border-slate-200 dark:border-slate-800 text-slate-400"
          }`}
        >
          <div
            className={`h-6 w-6 rounded-full flex items-center justify-center text-xs font-bold ${
              step === 1 ? "bg-teal-700 text-white" : step > 1 ? "bg-emerald-600 text-white" : "bg-slate-200 dark:bg-slate-800 text-slate-600"
            }`}
          >
            {step > 1 ? <CheckCircle className="h-3.5 w-3.5" /> : "1"}
          </div>
          <span className="text-xs font-semibold hidden sm:inline">Identity & Contact</span>
          <span className="text-xs font-semibold sm:hidden">Identity</span>
        </div>

        <div
          className={`flex items-center space-x-2 p-2.5 sm:p-3 rounded-lg border transition-all ${
            step === 2
              ? "border-teal-600 bg-teal-50/50 dark:bg-teal-950/40 text-teal-900 dark:text-teal-200 shadow-sm"
              : step > 2
              ? "border-emerald-300 bg-emerald-50/30 text-emerald-800 dark:border-emerald-800 dark:text-emerald-300"
              : "border-slate-200 dark:border-slate-800 text-slate-400"
          }`}
        >
          <div
            className={`h-6 w-6 rounded-full flex items-center justify-center text-xs font-bold ${
              step === 2 ? "bg-teal-700 text-white" : step > 2 ? "bg-emerald-600 text-white" : "bg-slate-200 dark:bg-slate-800 text-slate-600"
            }`}
          >
            {step > 2 ? <CheckCircle className="h-3.5 w-3.5" /> : "2"}
          </div>
          <span className="text-xs font-semibold hidden sm:inline">Curriculum & Campus</span>
          <span className="text-xs font-semibold sm:hidden">Curriculum</span>
        </div>

        <div
          className={`flex items-center space-x-2 p-2.5 sm:p-3 rounded-lg border transition-all ${
            step === 3
              ? "border-teal-600 bg-teal-50/50 dark:bg-teal-950/40 text-teal-900 dark:text-teal-200 shadow-sm"
              : "border-slate-200 dark:border-slate-800 text-slate-400"
          }`}
        >
          <div
            className={`h-6 w-6 rounded-full flex items-center justify-center text-xs font-bold ${
              step === 3 ? "bg-teal-700 text-white" : "bg-slate-200 dark:bg-slate-800 text-slate-600"
            }`}
          >
            3
          </div>
          <span className="text-xs font-semibold hidden sm:inline">Grades & Launch</span>
          <span className="text-xs font-semibold sm:hidden">Grades</span>
        </div>
      </div>

      {/* Main Wizard Form Card */}
      <Card className="border-slate-200 dark:border-slate-800 shadow-md">
        <CardHeader>
          <CardTitle className="text-lg">
            {step === 1 && "Step 1: School Identity & Regulatory Info"}
            {step === 2 && "Step 2: Educational Stream & Campus Location"}
            {step === 3 && "Step 3: Academic Session & Initial Class Hierarchy"}
          </CardTitle>
          <CardDescription className="text-xs">
            {step === 1 && "Define the school name, unique institutional code, and official communication channels."}
            {step === 2 && "Configure the Pakistani educational system and geographic location."}
            {step === 3 && "Confirm the inaugural academic session and the starting grade divisions."}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {errorMessage && (
            <div className="mb-5 p-3 rounded-md bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900 text-xs text-red-700 dark:text-red-300">
              {errorMessage}
            </div>
          )}

          {/* STEP 1: IDENTITY */}
          {step === 1 && (
            <div className="space-y-4">
              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                  School / Campus Full Name *
                </label>
                <div className="relative">
                  <SchoolIcon className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => {
                      setName(e.target.value);
                      if (!code) {
                        const words = e.target.value.trim().split(" ");
                        if (words.length >= 2) {
                          setCode(words.map((w) => w[0]).join("").toUpperCase() + "-01");
                        }
                      }
                    }}
                    placeholder="e.g. Islamabad Model College for Boys"
                    className="w-full pl-9 pr-3 py-2 text-sm rounded-md border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-600"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                    Institutional Campus Code *
                  </label>
                  <div className="relative">
                    <Building className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
                    <input
                      type="text"
                      required
                      value={code}
                      onChange={(e) => setCode(e.target.value.toUpperCase())}
                      placeholder="e.g. IMCB-F8"
                      className="w-full pl-9 pr-3 py-2 text-sm uppercase rounded-md border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-600"
                    />
                  </div>
                  <p className="text-[11px] text-slate-400">Unique alphanumeric tenant identifier (e.g. BSS-01)</p>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                    Registration / PEIRA / BISE #
                  </label>
                  <input
                    type="text"
                    value={registrationNumber}
                    onChange={(e) => setRegistrationNumber(e.target.value)}
                    placeholder="e.g. PEIRA/REG/2026/892"
                    className="w-full px-3 py-2 text-sm rounded-md border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-600"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                    Official Contact Email
                  </label>
                  <input
                    type="email"
                    value={contactEmail}
                    onChange={(e) => setContactEmail(e.target.value)}
                    placeholder="info@school.edu.pk"
                    className="w-full px-3 py-2 text-sm rounded-md border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-600"
                  />
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                    Official Contact Phone
                  </label>
                  <input
                    type="text"
                    value={phoneNumber}
                    onChange={(e) => setPhoneNumber(e.target.value)}
                    placeholder="+92 51 9260000"
                    className="w-full px-3 py-2 text-sm rounded-md border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-600"
                  />
                </div>
              </div>
            </div>
          )}

          {/* STEP 2: CURRICULUM & CAMPUS */}
          {step === 2 && (
            <div className="space-y-5">
              <div className="space-y-2">
                <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                  Select Educational Curriculum Stream *
                </label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {CURRICULUM_OPTIONS.map((opt) => (
                    <div
                      key={opt.id}
                      onClick={() => handleCurriculumSelect(opt.id)}
                      className={`cursor-pointer p-3.5 rounded-lg border text-left transition-all ${
                        curriculumType === opt.id
                          ? "border-teal-600 bg-teal-50/50 dark:bg-teal-950/40 ring-1 ring-teal-600 shadow-sm"
                          : "border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700"
                      }`}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs font-bold text-slate-900 dark:text-white">{opt.label}</span>
                        {curriculumType === opt.id && <CheckCircle className="h-4 w-4 text-teal-600" />}
                      </div>
                      <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-snug">{opt.description}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                    Province / Region *
                  </label>
                  <select
                    value={province}
                    onChange={(e) => setProvince(e.target.value)}
                    className="w-full px-3 py-2 text-sm rounded-md border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-600"
                  >
                    {PROVINCE_OPTIONS.map((prov) => (
                      <option key={prov.id} value={prov.id}>
                        {prov.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                    City / District *
                  </label>
                  <div className="relative">
                    <MapPin className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
                    <input
                      type="text"
                      required
                      value={city}
                      onChange={(e) => setCity(e.target.value)}
                      placeholder="e.g. Islamabad, Lahore, Karachi"
                      className="w-full pl-9 pr-3 py-2 text-sm rounded-md border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-600"
                    />
                  </div>
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                  Campus Physical Address
                </label>
                <textarea
                  rows={2}
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  placeholder="Street, Sector/Block, Campus Road..."
                  className="w-full px-3 py-2 text-sm rounded-md border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-600"
                />
              </div>
            </div>
          )}

          {/* STEP 3: ACADEMIC SESSIONS & GRADES */}
          {step === 3 && (
            <div className="space-y-5">
              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                  Initial Academic Session Name *
                </label>
                <div className="relative">
                  <BookOpen className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
                  <input
                    type="text"
                    required
                    value={academicYearName}
                    onChange={(e) => setAcademicYearName(e.target.value)}
                    placeholder="e.g. 2026-2027"
                    className="w-full pl-9 pr-3 py-2 text-sm rounded-md border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-600"
                  />
                </div>
                <p className="text-[11px] text-slate-400">Designates the primary active school year for student enrollments.</p>
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                    Grade Levels to Initialize ({selectedClasses.length} selected)
                  </label>
                  <span className="text-[11px] text-slate-400">Each class will receive an initial "Section A"</span>
                </div>

                <div className="flex flex-wrap gap-2 p-3 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50">
                  {CURRICULUM_OPTIONS.find((c) => c.id === curriculumType)?.defaultClasses.map((cls) => {
                    const isSelected = selectedClasses.includes(cls);
                    return (
                      <button
                        key={cls}
                        type="button"
                        onClick={() => handleToggleClass(cls)}
                        className={`text-xs px-3 py-1.5 rounded-md font-medium transition-all ${
                          isSelected
                            ? "bg-teal-700 text-white shadow-sm"
                            : "bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 hover:border-slate-300"
                        }`}
                      >
                        {isSelected && <CheckCircle className="inline h-3 w-3 mr-1" />}
                        {cls}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Tenant Summary Preview */}
              <div className="p-4 rounded-lg bg-teal-50/60 dark:bg-teal-950/40 border border-teal-200 dark:border-teal-800 space-y-2">
                <div className="flex items-center space-x-2 text-xs font-bold text-teal-900 dark:text-teal-200">
                  <GraduationCap className="h-4 w-4" />
                  <span>Ready to Provision School Tenant</span>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
                  <div>
                    <span className="text-slate-500 dark:text-slate-400 block text-[10px]">Institution</span>
                    <span className="font-semibold text-slate-900 dark:text-white truncate block">{name}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 dark:text-slate-400 block text-[10px]">Code</span>
                    <span className="font-semibold text-slate-900 dark:text-white block">{code}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 dark:text-slate-400 block text-[10px]">Session</span>
                    <span className="font-semibold text-slate-900 dark:text-white block">{academicYearName}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 dark:text-slate-400 block text-[10px]">Your Role</span>
                    <Badge variant="success" className="text-[10px]">School Owner</Badge>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Wizard Action Buttons */}
          <div className="flex items-center justify-between pt-6 mt-6 border-t border-slate-100 dark:border-slate-800">
            {step > 1 ? (
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={handlePrev}
                disabled={isLoading}
                className="flex items-center space-x-1"
              >
                <ArrowLeft className="h-4 w-4" />
                <span>Previous</span>
              </Button>
            ) : (
              <div />
            )}

            {step < 3 ? (
              <Button
                type="button"
                size="sm"
                onClick={handleNext}
                className="bg-teal-700 hover:bg-teal-800 text-white flex items-center space-x-1.5"
              >
                <span>Continue</span>
                <ArrowRight className="h-4 w-4" />
              </Button>
            ) : (
              <Button
                type="button"
                size="sm"
                onClick={handleSubmit}
                disabled={isLoading}
                className="bg-teal-700 hover:bg-teal-800 text-white flex items-center space-x-2"
              >
                {isLoading ? (
                  <div className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <>
                    <Rocket className="h-4 w-4" />
                    <span>Launch School Workspace</span>
                  </>
                )}
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default SchoolSetupWizard;

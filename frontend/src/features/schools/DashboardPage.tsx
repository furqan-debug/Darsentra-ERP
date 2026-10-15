import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  BarChart3,
  BookOpen,
  Building2,
  CalendarCheck,
  CheckCircle2,
  FileCheck2,
  GraduationCap,
  Layers,
  MapPin,
  Plus,
  Receipt,
  RefreshCw,
  School as SchoolIcon,
  Shield,
  Sparkles,
  UserCheck,
  Users,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/context/AuthContext";
import academicsService from "@/services/academicsService";
import type { AcademicClass } from "@/types/academics";

export const DashboardPage: React.FC = () => {
  const { user, activeSchool, activeRoleDisplay, schoolStats, refreshActiveSchool } = useAuth();

  const [classes, setClasses] = useState<AcademicClass[]>([]);
  const [isLoadingClasses, setIsLoadingClasses] = useState(false);
  const [activeTab, setActiveTab] = useState<"academics" | "overview" | "modules">("academics");

  // New Class Form State
  const [showAddClass, setShowAddClass] = useState(false);
  const [newClassName, setNewClassName] = useState("");
  const [newClassCode, setNewClassCode] = useState("");
  const [isSubmittingClass, setIsSubmittingClass] = useState(false);

  // New Section State
  const [activeClassForSection, setActiveClassForSection] = useState<string | null>(null);
  const [newSectionName, setNewSectionName] = useState("");
  const [newSectionCapacity, setNewSectionCapacity] = useState(40);
  const [isSubmittingSection, setIsSubmittingSection] = useState(false);

  const fetchClasses = async () => {
    setIsLoadingClasses(true);
    try {
      const data = await academicsService.getClasses();
      setClasses(data);
    } catch {
      // Handled
    } finally {
      setIsLoadingClasses(false);
    }
  };

  useEffect(() => {
    fetchClasses();
  }, [activeSchool?.id]);

  const handleCreateClass = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newClassName.trim()) return;

    setIsSubmittingClass(true);
    try {
      await academicsService.createClass({
        name: newClassName.trim(),
        code: newClassCode.trim() || undefined,
        order: classes.length + 1,
      });
      setNewClassName("");
      setNewClassCode("");
      setShowAddClass(false);
      await fetchClasses();
      await refreshActiveSchool();
    } catch {
      // Handled
    } finally {
      setIsSubmittingClass(false);
    }
  };

  const handleCreateSection = async (classId: string) => {
    if (!newSectionName.trim()) return;

    setIsSubmittingSection(true);
    try {
      await academicsService.createSection({
        academic_class: classId,
        name: newSectionName.trim(),
        capacity: Number(newSectionCapacity) || 40,
      });
      setNewSectionName("");
      setActiveClassForSection(null);
      await fetchClasses();
      await refreshActiveSchool();
    } catch {
      // Handled
    } finally {
      setIsSubmittingSection(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* School Header Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-teal-900 via-teal-800 to-slate-900 text-white p-6 sm:p-8 shadow-xl">
        <div className="absolute right-0 top-0 bottom-0 opacity-10 flex items-center pr-8 pointer-events-none">
          <Building2 className="w-80 h-80" />
        </div>

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-3 max-w-2xl">
            <div className="flex flex-wrap items-center gap-2">
              <Badge className="bg-teal-700/80 hover:bg-teal-700 text-white border-teal-500/30 text-xs px-2.5 py-0.5">
                <SchoolIcon className="h-3.5 w-3.5 mr-1" />
                Active Campus: {activeSchool?.code || "N/A"}
              </Badge>
              <Badge className="bg-white/10 hover:bg-white/20 text-teal-200 border-white/20 text-xs px-2.5 py-0.5">
                Session {schoolStats?.active_session || "2026-2027"}
              </Badge>
              <Badge className="bg-emerald-500/20 text-emerald-300 border-emerald-500/30 text-xs px-2.5 py-0.5">
                <CheckCircle2 className="h-3.5 w-3.5 mr-1 text-emerald-400" />
                {activeRoleDisplay || "School Administrator"}
              </Badge>
            </div>

            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight">
              {activeSchool?.name || "School Workspace"}
            </h1>

            <div className="flex flex-wrap items-center gap-4 text-xs text-teal-100">
              <span className="flex items-center">
                <MapPin className="h-3.5 w-3.5 mr-1 text-teal-300" />
                {activeSchool?.city}, {activeSchool?.province_display || activeSchool?.province}
              </span>
              <span>&bull;</span>
              <span className="flex items-center">
                <BookOpen className="h-3.5 w-3.5 mr-1 text-teal-300" />
                {activeSchool?.curriculum_display || activeSchool?.curriculum_type}
              </span>
              {activeSchool?.registration_number && (
                <>
                  <span>&bull;</span>
                  <span>Reg: {activeSchool.registration_number}</span>
                </>
              )}
            </div>
          </div>

          <div className="flex flex-wrap md:flex-col items-start md:items-end gap-2.5">
            <Link to="/setup-school">
              <Button
                variant="outline"
                size="sm"
                className="bg-white/10 hover:bg-white/20 text-white border-white/20 text-xs flex items-center space-x-1.5"
              >
                <Plus className="h-3.5 w-3.5" />
                <span>Add Another Campus</span>
              </Button>
            </Link>
            <div className="text-[11px] text-teal-200/80">
              Logged in as <span className="font-semibold text-white">{user?.full_name || user?.email}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="border-slate-200 dark:border-slate-800 shadow-sm">
          <CardContent className="p-5 flex items-center justify-between">
            <div className="space-y-1">
              <span className="text-xs font-medium text-slate-500 dark:text-slate-400">Total Students</span>
              <div className="text-2xl font-bold text-slate-900 dark:text-white">
                {schoolStats?.total_students ?? 0}
              </div>
              <span className="text-[11px] text-teal-700 dark:text-teal-400 font-medium">Admissions Ready</span>
            </div>
            <div className="h-11 w-11 rounded-xl bg-teal-50 dark:bg-teal-950/60 text-teal-700 dark:text-teal-400 flex items-center justify-center">
              <GraduationCap className="h-6 w-6" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-slate-200 dark:border-slate-800 shadow-sm">
          <CardContent className="p-5 flex items-center justify-between">
            <div className="space-y-1">
              <span className="text-xs font-medium text-slate-500 dark:text-slate-400">Faculty & Staff</span>
              <div className="text-2xl font-bold text-slate-900 dark:text-white">
                {schoolStats?.total_staff ?? 1}
              </div>
              <span className="text-[11px] text-emerald-600 font-medium">1 Active (Owner)</span>
            </div>
            <div className="h-11 w-11 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-400 flex items-center justify-center">
              <UserCheck className="h-6 w-6" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-slate-200 dark:border-slate-800 shadow-sm">
          <CardContent className="p-5 flex items-center justify-between">
            <div className="space-y-1">
              <span className="text-xs font-medium text-slate-500 dark:text-slate-400">Academic Classes</span>
              <div className="text-2xl font-bold text-slate-900 dark:text-white">
                {classes.length || schoolStats?.total_classes || 0}
              </div>
              <span className="text-[11px] text-blue-600 font-medium">Configured Grades</span>
            </div>
            <div className="h-11 w-11 rounded-xl bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-400 flex items-center justify-center">
              <Layers className="h-6 w-6" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-slate-200 dark:border-slate-800 shadow-sm">
          <CardContent className="p-5 flex items-center justify-between">
            <div className="space-y-1">
              <span className="text-xs font-medium text-slate-500 dark:text-slate-400">Class Sections</span>
              <div className="text-2xl font-bold text-slate-900 dark:text-white">
                {classes.reduce((sum, c) => sum + (c.section_count || c.sections?.length || 0), 0) || schoolStats?.total_sections || 0}
              </div>
              <span className="text-[11px] text-purple-600 font-medium">Active Cohorts</span>
            </div>
            <div className="h-11 w-11 rounded-xl bg-purple-50 dark:bg-purple-950/60 text-purple-700 dark:text-purple-400 flex items-center justify-center">
              <Users className="h-6 w-6" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center space-x-2 border-b border-slate-200 dark:border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab("academics")}
          className={`flex items-center space-x-2 px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
            activeTab === "academics"
              ? "bg-teal-700 text-white"
              : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
          }`}
        >
          <Layers className="h-3.5 w-3.5" />
          <span>Academics & Classes</span>
          <span className="ml-1 px-1.5 py-0.2 rounded-full text-[10px] bg-white/20">
            {classes.length}
          </span>
        </button>

        <button
          onClick={() => setActiveTab("overview")}
          className={`flex items-center space-x-2 px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
            activeTab === "overview"
              ? "bg-teal-700 text-white"
              : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
          }`}
        >
          <Shield className="h-3.5 w-3.5" />
          <span>Tenant Scoping & Security</span>
        </button>

        <button
          onClick={() => setActiveTab("modules")}
          className={`flex items-center space-x-2 px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
            activeTab === "modules"
              ? "bg-teal-700 text-white"
              : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
          }`}
        >
          <Sparkles className="h-3.5 w-3.5" />
          <span>ERP Modules Hub</span>
        </button>
      </div>

      {/* TAB 1: ACADEMICS HIERARCHY */}
      {activeTab === "academics" && (
        <Card className="border-slate-200 dark:border-slate-800 shadow-sm">
          <CardHeader className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-100 dark:border-slate-800 pb-4">
            <div>
              <div className="flex items-center space-x-2">
                <Layers className="h-5 w-5 text-teal-700" />
                <CardTitle className="text-base">Grade Levels & Classroom Sections</CardTitle>
              </div>
              <CardDescription className="text-xs">
                Manage the active grades and classroom cohort divisions for this school campus.
              </CardDescription>
            </div>

            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={fetchClasses}
                disabled={isLoadingClasses}
                className="text-xs flex items-center space-x-1"
              >
                <RefreshCw className={`h-3 w-3 ${isLoadingClasses ? "animate-spin" : ""}`} />
                <span>Refresh</span>
              </Button>

              <Button
                size="sm"
                onClick={() => setShowAddClass(!showAddClass)}
                className="bg-teal-700 hover:bg-teal-800 text-white text-xs flex items-center space-x-1"
              >
                <Plus className="h-3.5 w-3.5" />
                <span>Add Class Grade</span>
              </Button>
            </div>
          </CardHeader>

          <CardContent className="pt-6 space-y-6">
            {/* Inline Add Class Form */}
            {showAddClass && (
              <form
                onSubmit={handleCreateClass}
                className="p-4 rounded-xl border border-teal-200 dark:border-teal-800 bg-teal-50/40 dark:bg-teal-950/20 space-y-3"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-teal-900 dark:text-teal-200">
                    Create New Academic Class
                  </span>
                  <button
                    type="button"
                    onClick={() => setShowAddClass(false)}
                    className="text-xs text-slate-400 hover:text-slate-600"
                  >
                    Cancel
                  </button>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="text-[11px] font-semibold text-slate-700 dark:text-slate-300 block mb-1">
                      Class Name *
                    </label>
                    <input
                      type="text"
                      required
                      value={newClassName}
                      onChange={(e) => setNewClassName(e.target.value)}
                      placeholder="e.g. Class 11 / FSc Part 1 / O-3"
                      className="w-full px-3 py-1.5 text-xs rounded-md border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white"
                    />
                  </div>
                  <div>
                    <label className="text-[11px] font-semibold text-slate-700 dark:text-slate-300 block mb-1">
                      Class Code (Optional)
                    </label>
                    <input
                      type="text"
                      value={newClassCode}
                      onChange={(e) => setNewClassCode(e.target.value)}
                      placeholder="e.g. C-11"
                      className="w-full px-3 py-1.5 text-xs rounded-md border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white"
                    />
                  </div>
                </div>

                <div className="flex justify-end">
                  <Button
                    type="submit"
                    size="sm"
                    disabled={isSubmittingClass}
                    className="bg-teal-700 hover:bg-teal-800 text-white text-xs"
                  >
                    {isSubmittingClass ? "Saving..." : "Save Class"}
                  </Button>
                </div>
              </form>
            )}

            {/* Class Cards Grid */}
            {isLoadingClasses ? (
              <div className="text-center py-12 text-xs text-slate-500">
                <RefreshCw className="h-6 w-6 animate-spin mx-auto text-teal-600 mb-2" />
                Loading academic structure...
              </div>
            ) : classes.length === 0 ? (
              <div className="text-center py-12 border border-dashed rounded-xl p-8 space-y-3">
                <Layers className="h-10 w-10 mx-auto text-slate-400" />
                <h3 className="text-sm font-bold text-slate-800 dark:text-white">
                  No Classes Initialized
                </h3>
                <p className="text-xs text-slate-500 max-w-sm mx-auto">
                  Click "Add Class Grade" above to create your first academic grade level for this campus.
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {classes.map((cls) => (
                  <div
                    key={cls.id}
                    className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 shadow-sm space-y-3"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <div className="h-8 w-8 rounded-lg bg-teal-100 dark:bg-teal-900/40 text-teal-800 dark:text-teal-300 flex items-center justify-center text-xs font-bold">
                          {cls.order}
                        </div>
                        <div>
                          <div className="text-sm font-bold text-slate-900 dark:text-white">{cls.name}</div>
                          {cls.code && (
                            <span className="text-[10px] text-slate-400 font-mono">Code: {cls.code}</span>
                          )}
                        </div>
                      </div>

                      <Badge variant="outline" className="text-[10px]">
                        {cls.sections?.length || 0} Section{(cls.sections?.length || 0) !== 1 ? "s" : ""}
                      </Badge>
                    </div>

                    {/* Section Badges */}
                    <div className="pt-2 border-t border-slate-100 dark:border-slate-800 space-y-2">
                      <div className="flex items-center justify-between text-[11px]">
                        <span className="text-slate-500 font-medium">Sections:</span>
                        <button
                          type="button"
                          onClick={() => setActiveClassForSection(cls.id)}
                          className="text-teal-700 dark:text-teal-400 hover:underline font-semibold flex items-center space-x-0.5"
                        >
                          <Plus className="h-3 w-3" />
                          <span>Add Section</span>
                        </button>
                      </div>

                      <div className="flex flex-wrap gap-1.5">
                        {cls.sections && cls.sections.length > 0 ? (
                          cls.sections.map((sec) => (
                            <div
                              key={sec.id}
                              className="px-2.5 py-1 rounded bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 text-xs flex items-center space-x-1"
                            >
                              <span className="font-medium">{sec.name}</span>
                              <span className="text-[10px] text-slate-400">({sec.capacity} cap)</span>
                            </div>
                          ))
                        ) : (
                          <span className="text-xs text-slate-400 italic">No sections created</span>
                        )}
                      </div>

                      {/* Add Section Form under this class */}
                      {activeClassForSection === cls.id && (
                        <div className="mt-2 p-2.5 rounded bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-2">
                          <div className="text-[10px] font-semibold text-slate-700 dark:text-slate-200">
                            New Section for {cls.name}
                          </div>
                          <div className="grid grid-cols-2 gap-2">
                            <input
                              type="text"
                              value={newSectionName}
                              onChange={(e) => setNewSectionName(e.target.value)}
                              placeholder="e.g. Section B"
                              className="px-2 py-1 text-xs rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900"
                            />
                            <input
                              type="number"
                              value={newSectionCapacity}
                              onChange={(e) => setNewSectionCapacity(Number(e.target.value))}
                              placeholder="Capacity"
                              className="px-2 py-1 text-xs rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900"
                            />
                          </div>
                          <div className="flex justify-end space-x-1 pt-1">
                            <button
                              type="button"
                              onClick={() => setActiveClassForSection(null)}
                              className="px-2 py-0.5 text-[10px] text-slate-500"
                            >
                              Cancel
                            </button>
                            <Button
                              type="button"
                              size="sm"
                              disabled={isSubmittingSection}
                              onClick={() => handleCreateSection(cls.id)}
                              className="h-6 px-2 text-[10px] bg-teal-700 hover:bg-teal-800 text-white"
                            >
                              Add
                            </Button>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* TAB 2: TENANT SECURITY & SCOPE */}
      {activeTab === "overview" && (
        <Card className="border-slate-200 dark:border-slate-800 shadow-sm">
          <CardHeader>
            <div className="flex items-center space-x-2">
              <Shield className="h-5 w-5 text-teal-700" />
              <CardTitle className="text-base">Tenant Isolation Architecture</CardTitle>
            </div>
            <CardDescription className="text-xs">
              How Darsentra ERP protects your school records against multi-tenant data leaks.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 space-y-2">
                <span className="text-xs font-bold text-teal-800 dark:text-teal-300">Tenant Identity</span>
                <p className="text-xs text-slate-600 dark:text-slate-400">
                  Every query is anchored to <code className="bg-slate-200 dark:bg-slate-800 px-1 py-0.5 rounded text-[11px]">School ID: {activeSchool?.id}</code>. Cross-tenant access is structurally blocked at the ORM layer.
                </p>
              </div>

              <div className="p-4 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 space-y-2">
                <span className="text-xs font-bold text-teal-800 dark:text-teal-300">Request Validation</span>
                <p className="text-xs text-slate-600 dark:text-slate-400">
                  The client sends the <code className="bg-slate-200 dark:bg-slate-800 px-1 py-0.5 rounded text-[11px]">X-School-ID</code> header. The Django <code className="bg-slate-200 dark:bg-slate-800 px-1 py-0.5 rounded text-[11px]">TenantSecurityService</code> validates user membership before query execution.
                </p>
              </div>

              <div className="p-4 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 space-y-2">
                <span className="text-xs font-bold text-teal-800 dark:text-teal-300">Curriculum Compliance</span>
                <p className="text-xs text-slate-600 dark:text-slate-400">
                  Current curriculum stream: <strong>{activeSchool?.curriculum_display}</strong>. Supports BISE (Federal, Punjab, Sindh, KPK, Balochistan) and Cambridge streams.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* TAB 3: ERP MODULES HUB */}
      {activeTab === "modules" && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            {
              title: "Student Admissions & Records",
              icon: GraduationCap,
              desc: "Manage Pakistani student profiles, Bay-Form/B-Form, father CNIC, emergency contacts, and class enrollments.",
              status: "Phase 3 Ready",
            },
            {
              title: "Daily Attendance Register",
              icon: CalendarCheck,
              desc: "Daily morning roll-call with SMS alerts to parents for absent/late students.",
              status: "Phase 3 Ready",
            },
            {
              title: "Fee Billing & Vouchers",
              icon: Receipt,
              desc: "Print 3-copy Pakistani bank challans (Student/School/Bank copy) and automated tuition arrears.",
              status: "Phase 3 Ready",
            },
            {
              title: "Examinations & BISE Gradebooks",
              icon: FileCheck2,
              desc: "Term tests, monthly assessments, BISE board style roll slips, and official printable transcripts.",
              status: "Phase 3 Ready",
            },
            {
              title: "Staff & Faculty Payroll",
              icon: UserCheck,
              desc: "Teacher profiles, subject allocation, monthly salaries, and staff attendance tracking.",
              status: "Phase 3 Ready",
            },
            {
              title: "Reports & Analytics",
              icon: BarChart3,
              desc: "PEIRA/BISE compliance summaries, daily fee collection ledger, and school performance KPIs.",
              status: "Phase 3 Ready",
            },
          ].map((mod) => {
            const Icon = mod.icon;
            return (
              <Card key={mod.title} className="border-slate-200 dark:border-slate-800 shadow-sm">
                <CardHeader className="p-5">
                  <div className="flex items-center justify-between mb-2">
                    <div className="h-9 w-9 rounded-lg bg-teal-100 dark:bg-teal-900/50 text-teal-800 dark:text-teal-300 flex items-center justify-center">
                      <Icon className="h-5 w-5" />
                    </div>
                    <Badge variant="secondary" className="text-[10px]">
                      {mod.status}
                    </Badge>
                  </div>
                  <CardTitle className="text-sm font-bold">{mod.title}</CardTitle>
                  <CardDescription className="text-xs">{mod.desc}</CardDescription>
                </CardHeader>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default DashboardPage;

import { useState } from "react";
import { Building2, Briefcase, Users, MapPin, DollarSign, TrendingUp, Zap, Target, Globe2, Loader2 } from "lucide-react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Switch } from "./ui/switch";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { toast } from "sonner";
import SMEReport, { ReportData } from "./SMEReport";

// ML-ready field metadata interface
interface FieldMetadata {
  ml_field: boolean;
  ml_name?: string;
  type?: "string" | "number" | "boolean" | "array";
}

// Profile interface with ML metadata
interface Profile {
  business_name: string;
  country: string;
  sector: string;
  employees: string;
  annual_revenue: string;
  tech_adoption_level: string;
  main_challenges: string[];
  digital_tools_used: string[];
  growth_last_yr: string;
  funding_status: string;
  female_owned: boolean;
  remote_work_policy: string;
}

// ==========================================
// ML FIELD CONFIGURATION FOR BACKEND/ML INTEGRATION
// ==========================================
// Fields with ml_field: true will be sent to ML models
// Fields with ml_field: false are for display/reporting only
const fieldConfig = {
  // NON-ML FIELDS (Display/Reporting Only)
  business_name: { 
    ml_field: false 
  } as FieldMetadata,

  // ML FIELDS (Sent to ML Models for Analysis)
  country: { 
    ml_field: true, 
    ml_name: "country", 
    type: "string" 
  } as FieldMetadata,
  
  sector: { 
    ml_field: true, 
    ml_name: "sector", 
    type: "string" 
  } as FieldMetadata,
  
  employees: { 
    ml_field: true, 
    ml_name: "employees", 
    type: "number" 
  } as FieldMetadata,
  
  annual_revenue: { 
    ml_field: true, 
    ml_name: "annual_revenue", 
    type: "number" 
  } as FieldMetadata,
  
  tech_adoption_level: { 
    ml_field: true, 
    ml_name: "tech_adoption_level", 
    type: "string" 
  } as FieldMetadata,
  
  main_challenges: { 
    ml_field: true, 
    ml_name: "main_challenges", 
    type: "array" 
  } as FieldMetadata,
  
  digital_tools_used: { 
    ml_field: true, 
    ml_name: "digital_tools_used", 
    type: "array" 
  } as FieldMetadata,
  
  growth_last_yr: { 
    ml_field: true, 
    ml_name: "growth_last_yr", 
    type: "number" 
  } as FieldMetadata,
  
  funding_status: { 
    ml_field: true, 
    ml_name: "funding_status", 
    type: "string" 
  } as FieldMetadata,
  
  female_owned: { 
    ml_field: true, 
    ml_name: "female_owned", 
    type: "boolean" 
  } as FieldMetadata,
  
  remote_work_policy: { 
    ml_field: true, 
    ml_name: "remote_work_policy", 
    type: "string" 
  } as FieldMetadata,
};

const SMEProfileBuilder = () => {
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [currentReport, setCurrentReport] = useState<ReportData | null>(null);
  const [isGeneratingReport, setIsGeneratingReport] = useState(false);
  const [isDemoMode, setIsDemoMode] = useState(false);
  const [formData, setFormData] = useState<Profile>({
    business_name: "",
    country: "",
    sector: "",
    employees: "",
    annual_revenue: "",
    tech_adoption_level: "",
    main_challenges: [],
    digital_tools_used: [],
    growth_last_yr: "",
    funding_status: "",
    female_owned: false,
    remote_work_policy: "",
  });

  // Demo data for testing
  const demoData: Profile = {
    business_name: "TechVentures Kenya Ltd",
    country: "Kenya",
    sector: "Technology",
    employees: "45",
    annual_revenue: "2500000",
    tech_adoption_level: "High",
    main_challenges: ["Funding", "Talent Acquisition"],
    digital_tools_used: ["Cloud Services", "CRM", "Project Management"],
    growth_last_yr: "35",
    funding_status: "Seed Funded",
    female_owned: true,
    remote_work_policy: "Hybrid",
  };

  const handleDemoToggle = (checked: boolean) => {
    setIsDemoMode(checked);
    if (checked) {
      setFormData(demoData);
      toast.success("Demo data loaded!");
    } else {
      setFormData({
        business_name: "",
        country: "",
        sector: "",
        employees: "",
        annual_revenue: "",
        tech_adoption_level: "",
        main_challenges: [],
        digital_tools_used: [],
        growth_last_yr: "",
        funding_status: "",
        female_owned: false,
        remote_work_policy: "",
      });
      toast.info("Demo mode disabled");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGeneratingReport(true);
    
    try {
      // ==========================================
      // ML PAYLOAD PREPARATION
      // ==========================================
      // Extract only ML fields for backend/ML model processing
      const mlPayload: any = {};
      Object.entries(formData).forEach(([key, value]) => {
        const config = fieldConfig[key as keyof typeof fieldConfig];
        if (config.ml_field && config.ml_name) {
          mlPayload[config.ml_name] = value;
        }
      });

      console.log("🤖 ML Payload (sent to ML models):", mlPayload);
      console.log("📋 Full Form Data (for reporting):", formData);

      // TODO: Replace with actual Django API call
      // const response = await fetch('http://django-backend/api/profiles/', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ 
      //     profile_data: formData,        // Full profile for reporting
      //     ml_features: mlPayload         // ML fields only for model input
      //   })
      // });
      // const profileData = await response.json();
      
      setProfiles([...profiles, formData]);
      toast.success("✅ Profile submitted successfully!");
      
      // Simulate ML model processing
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Generate report with new sections
      const mockReport: ReportData = {
        businessName: formData.business_name,
        profile: {
          business_name: formData.business_name,
          sector: formData.sector,
          country: formData.country,
          female_owned: formData.female_owned,
          remote_work_policy: formData.remote_work_policy,
        },
        financialSnapshot: {
          employees: parseInt(formData.employees) || 0,
          annual_revenue: parseInt(formData.annual_revenue) || 0,
          growth_last_yr: parseFloat(formData.growth_last_yr) || 0,
          funding_status: formData.funding_status,
        },
        techOperations: {
          tech_adoption_level: formData.tech_adoption_level,
          digital_tools_used: formData.digital_tools_used,
          main_challenges: formData.main_challenges,
        },
        summary: `${formData.business_name} is a ${formData.female_owned ? 'woman-owned' : ''} ${formData.sector} business in ${formData.country} with ${formData.employees} employees. With an annual revenue of $${parseInt(formData.annual_revenue).toLocaleString()}, the company has achieved ${formData.growth_last_yr}% growth last year. The business maintains a ${formData.remote_work_policy} work policy and shows ${formData.tech_adoption_level} technology adoption.`,
        suggestions: [
          `Given your ${formData.tech_adoption_level} tech adoption, consider integrating AI-powered analytics to optimize operations.`,
          `With ${formData.employees} employees, invest in comprehensive training programs to boost productivity.`,
          `Your ${formData.growth_last_yr}% growth rate is promising - explore scaling opportunities in adjacent markets.`,
          `Address key challenges: ${formData.main_challenges.join(", ")} through strategic partnerships.`,
          `Leverage your ${formData.digital_tools_used.join(", ")} stack for data-driven decision making.`
        ],
        complianceScore: Math.floor(Math.random() * 30) + 65,
        sectorAverage: formData.sector === "Technology" ? 78 : formData.sector === "Retail" ? 72 : 75,
        historicalScores: [
          { date: "Q1 2024", score: 60 },
          { date: "Q2 2024", score: 68 },
          { date: "Q3 2024", score: 73 },
          { date: "Q4 2024", score: Math.floor(Math.random() * 30) + 65 }
        ],
        generatedAt: new Date().toISOString()
      };
      
      setCurrentReport(mockReport);
      toast.success("📊 Report generated successfully!");
      setIsDemoMode(false);
      
      // Reset form
      setFormData({
        business_name: "",
        country: "",
        sector: "",
        employees: "",
        annual_revenue: "",
        tech_adoption_level: "",
        main_challenges: [],
        digital_tools_used: [],
        growth_last_yr: "",
        funding_status: "",
        female_owned: false,
        remote_work_policy: "",
      });
    } catch (error) {
      toast.error("Failed to generate report. Please try again.");
      console.error("Report generation error:", error);
    } finally {
      setIsGeneratingReport(false);
    }
  };

  return (
    <div className="space-y-8">
      {currentReport ? (
        <div className="space-y-6">
          <Button 
            onClick={() => setCurrentReport(null)} 
            variant="outline"
            className="mb-4"
          >
            ← Create New Profile
          </Button>
          <SMEReport report={currentReport} />
        </div>
      ) : (
        <>
          <Card className="max-w-4xl mx-auto shadow-card">
        <CardHeader className="gradient-hero text-primary-foreground rounded-t-xl">
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-2xl flex items-center gap-2">
                <Building2 className="h-6 w-6" />
                📋 SME Profile Builder
              </CardTitle>
              <CardDescription className="text-primary-foreground/80 mt-1">
                Build your business profile for ML-powered insights
              </CardDescription>
            </div>
            <div className="flex items-center gap-3 bg-primary-foreground/10 px-4 py-2 rounded-lg">
              <Label htmlFor="demo-mode" className="text-primary-foreground text-sm font-medium cursor-pointer">
                Demo Mode
              </Label>
              <Switch
                id="demo-mode"
                checked={isDemoMode}
                onCheckedChange={handleDemoToggle}
              />
            </div>
          </div>
        </CardHeader>
        <CardContent className="p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Section 1: Basic Information */}
            <div className="space-y-1">
              <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
                <Building2 className="h-5 w-5 text-primary" />
                Basic Information
              </h3>
              <p className="text-sm text-muted-foreground">Core business details</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="business_name" className="flex items-center gap-2">
                  <Building2 className="h-4 w-4 text-primary" />
                  Business Name
                  <Badge variant="outline" className="ml-auto text-xs">Display Only</Badge>
                </Label>
                <Input
                  id="business_name"
                  value={formData.business_name}
                  onChange={(e) => setFormData({ ...formData, business_name: e.target.value })}
                  required
                  placeholder="Enter business name"
                />
                <p className="text-xs text-muted-foreground">Not used in ML analysis</p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="country" className="flex items-center gap-2">
                  <Globe2 className="h-4 w-4 text-primary" />
                  Country
                  <Badge variant="secondary" className="ml-auto text-xs bg-green-500/10 text-green-600 dark:text-green-400">ML Field</Badge>
                </Label>
                <Select value={formData.country} onValueChange={(value) => setFormData({ ...formData, country: value })}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select country" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Kenya">Kenya</SelectItem>
                    <SelectItem value="Uganda">Uganda</SelectItem>
                    <SelectItem value="Tanzania">Tanzania</SelectItem>
                    <SelectItem value="Rwanda">Rwanda</SelectItem>
                    <SelectItem value="Other">Other</SelectItem>
                  </SelectContent>
                </Select>
                <p className="text-xs text-muted-foreground">Used by ML models for regional analysis</p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="sector" className="flex items-center gap-2">
                  <Briefcase className="h-4 w-4 text-primary" />
                  Sector
                  <Badge variant="secondary" className="ml-auto text-xs bg-green-500/10 text-green-600 dark:text-green-400">ML Field</Badge>
                </Label>
                <Select value={formData.sector} onValueChange={(value) => setFormData({ ...formData, sector: value })}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select sector" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Agriculture">Agriculture</SelectItem>
                    <SelectItem value="Retail">Retail</SelectItem>
                    <SelectItem value="Manufacturing">Manufacturing</SelectItem>
                    <SelectItem value="Services">Services</SelectItem>
                    <SelectItem value="Technology">Technology</SelectItem>
                    <SelectItem value="Health">Health</SelectItem>
                    <SelectItem value="Food">Food & Beverage</SelectItem>
                  </SelectContent>
                </Select>
                <p className="text-xs text-muted-foreground">Used by ML models for sector-specific insights</p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="employees" className="flex items-center gap-2">
                  <Users className="h-4 w-4 text-primary" />
                  Employee Count
                  <Badge variant="secondary" className="ml-auto text-xs bg-green-500/10 text-green-600 dark:text-green-400">ML Field</Badge>
                </Label>
                <Input
                  id="employees"
                  type="number"
                  min="0"
                  value={formData.employees}
                  onChange={(e) => setFormData({ ...formData, employees: e.target.value })}
                  placeholder="e.g. 25"
                />
                <p className="text-xs text-muted-foreground">Used by ML models for business size classification</p>
              </div>
            </div>

            {/* Section 2: Financial Information */}
            <div className="space-y-1 pt-4">
              <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
                <DollarSign className="h-5 w-5 text-primary" />
                Financial Information
              </h3>
              <p className="text-sm text-muted-foreground">Revenue and growth metrics</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="annual_revenue" className="flex items-center gap-2">
                  <DollarSign className="h-4 w-4 text-primary" />
                  Annual Revenue (USD)
                  <Badge variant="secondary" className="ml-auto text-xs bg-green-500/10 text-green-600 dark:text-green-400">ML Field</Badge>
                </Label>
                <Input
                  id="annual_revenue"
                  type="number"
                  min="0"
                  value={formData.annual_revenue}
                  onChange={(e) => setFormData({ ...formData, annual_revenue: e.target.value })}
                  placeholder="e.g. 500000"
                />
                <p className="text-xs text-muted-foreground">Used by ML models for financial health scoring</p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="growth_last_yr" className="flex items-center gap-2">
                  <TrendingUp className="h-4 w-4 text-primary" />
                  Growth Last Year (%)
                  <Badge variant="secondary" className="ml-auto text-xs bg-green-500/10 text-green-600 dark:text-green-400">ML Field</Badge>
                </Label>
                <Input
                  id="growth_last_yr"
                  type="number"
                  step="0.1"
                  value={formData.growth_last_yr}
                  onChange={(e) => setFormData({ ...formData, growth_last_yr: e.target.value })}
                  placeholder="e.g. 15.5"
                />
                <p className="text-xs text-muted-foreground">Used by ML models for growth trajectory analysis</p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="funding_status" className="flex items-center gap-2">
                  <Target className="h-4 w-4 text-primary" />
                  Funding Status
                  <Badge variant="secondary" className="ml-auto text-xs bg-green-500/10 text-green-600 dark:text-green-400">ML Field</Badge>
                </Label>
                <Select value={formData.funding_status} onValueChange={(value) => setFormData({ ...formData, funding_status: value })}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Bootstrapped">Bootstrapped</SelectItem>
                    <SelectItem value="Seed Funded">Seed Funded</SelectItem>
                    <SelectItem value="Series A">Series A</SelectItem>
                    <SelectItem value="Series B+">Series B+</SelectItem>
                    <SelectItem value="Not Seeking">Not Seeking Funding</SelectItem>
                  </SelectContent>
                </Select>
                <p className="text-xs text-muted-foreground">Used by ML models for funding opportunity matching</p>
              </div>
            </div>

            {/* Section 3: Technology & Operations */}
            <div className="space-y-1 pt-4">
              <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
                <Zap className="h-5 w-5 text-primary" />
                Technology & Operations
              </h3>
              <p className="text-sm text-muted-foreground">Digital maturity and tools</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="tech_adoption_level" className="flex items-center gap-2">
                  <Zap className="h-4 w-4 text-primary" />
                  Tech Adoption Level
                  <Badge variant="secondary" className="ml-auto text-xs bg-green-500/10 text-green-600 dark:text-green-400">ML Field</Badge>
                </Label>
                <Select value={formData.tech_adoption_level} onValueChange={(value) => setFormData({ ...formData, tech_adoption_level: value })}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select level" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Low">Low - Basic digital tools</SelectItem>
                    <SelectItem value="Medium">Medium - Some automation</SelectItem>
                    <SelectItem value="High">High - Advanced tech stack</SelectItem>
                  </SelectContent>
                </Select>
                <p className="text-xs text-muted-foreground">Used by ML models for digital maturity assessment</p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="remote_work_policy" className="flex items-center gap-2">
                  <Users className="h-4 w-4 text-primary" />
                  Remote Work Policy
                  <Badge variant="secondary" className="ml-auto text-xs bg-green-500/10 text-green-600 dark:text-green-400">ML Field</Badge>
                </Label>
                <Select value={formData.remote_work_policy} onValueChange={(value) => setFormData({ ...formData, remote_work_policy: value })}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select policy" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="On-site">On-site Only</SelectItem>
                    <SelectItem value="Hybrid">Hybrid</SelectItem>
                    <SelectItem value="Remote">Fully Remote</SelectItem>
                  </SelectContent>
                </Select>
                <p className="text-xs text-muted-foreground">Used by ML models for operational flexibility scoring</p>
              </div>

              <div className="space-y-2">
                <Label className="flex items-center gap-2">
                  <Building2 className="h-4 w-4 text-primary" />
                  Female Owned
                  <Badge variant="secondary" className="ml-auto text-xs bg-green-500/10 text-green-600 dark:text-green-400">ML Field</Badge>
                </Label>
                <div className="flex items-center space-x-3 h-10">
                  <Switch
                    id="female_owned"
                    checked={formData.female_owned}
                    onCheckedChange={(checked) => setFormData({ ...formData, female_owned: checked })}
                  />
                  <Label htmlFor="female_owned" className="cursor-pointer text-sm">
                    {formData.female_owned ? "Yes" : "No"}
                  </Label>
                </div>
                <p className="text-xs text-muted-foreground">Used by ML models for diversity program matching</p>
              </div>
            </div>

            <Button 
              type="submit" 
              className="w-full gradient-hero" 
              disabled={isGeneratingReport}
            >
              {isGeneratingReport ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Generating Report...
                </>
              ) : (
                "Submit & Generate Report"
              )}
            </Button>
          </form>
        </CardContent>
      </Card>

      {profiles.length > 0 && (
        <div className="max-w-7xl mx-auto mt-8">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <Building2 className="h-6 w-6 text-primary" />
            📊 Submitted Profiles
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {profiles.map((profile, index) => (
              <Card key={index} className="shadow-card hover:shadow-hover transition-shadow">
                <CardHeader>
                  <CardTitle className="flex items-center justify-between text-lg">
                    <span className="flex items-center gap-2">
                      <Building2 className="h-5 w-5 text-primary" />
                      {profile.business_name}
                    </span>
                    {profile.female_owned && (
                      <Badge variant="secondary" className="text-xs">Woman-Owned</Badge>
                    )}
                  </CardTitle>
                  <CardDescription>
                    {profile.sector} • {profile.country}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-2 text-sm">
                  <p><strong>Employees:</strong> {profile.employees}</p>
                  <p><strong>Revenue:</strong> ${parseInt(profile.annual_revenue).toLocaleString()}</p>
                  <p><strong>Growth:</strong> {profile.growth_last_yr}%</p>
                  <p><strong>Tech Level:</strong> {profile.tech_adoption_level}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}
        </>
      )}
    </div>
  );
};

export default SMEProfileBuilder;

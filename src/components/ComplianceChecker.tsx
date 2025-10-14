import { useState } from "react";
import { CheckCircle2, AlertCircle, Download, Upload, FileCheck, Building2, Users, Briefcase, MapPin, UserCheck } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Badge } from "./ui/badge";
import { Switch } from "./ui/switch";
import { Label } from "./ui/label";
import { Input } from "./ui/input";
import { Progress } from "./ui/progress";
import { toast } from "sonner";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import html2pdf from "html2pdf.js";

interface ComplianceItem {
  id: string;
  name: string;
  description: string;
  status: "required" | "recommended" | "optional";
  completionStatus: "pending" | "done";
  uploadedFile?: {
    name: string;
    type: string;
    timestamp: number;
  };
}

const ComplianceChecker = () => {
  const [businessName, setBusinessName] = useState("");
  const [businessType, setBusinessType] = useState("");
  const [sector, setSector] = useState("");
  const [region, setRegion] = useState("");
  const [hasEmployees, setHasEmployees] = useState(false);
  const [ownerCategory, setOwnerCategory] = useState("");
  const [hasECitizen, setHasECitizen] = useState(false);
  const [hasBankAccount, setHasBankAccount] = useState(false);
  const [complianceItems, setComplianceItems] = useState<ComplianceItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sectorBenchmark, setSectorBenchmark] = useState(75);

  // TODO: Replace with actual API call to Django backend
  const checkCompliance = async () => {
    if (!businessName || !businessType || !sector || !region) {
      toast.error("Please fill in all required fields");
      return;
    }

    setIsLoading(true);
    
    // Simulated API call - replace with actual backend integration
    setTimeout(() => {
      const mockData: ComplianceItem[] = [
        {
          id: "1",
          name: "Business Registration Certificate",
          description: "Register your business with the Business Registration Service (BRS)",
          status: "required",
          completionStatus: "pending"
        },
        {
          id: "2",
          name: "KRA PIN Certificate",
          description: "Obtain a Personal Identification Number from Kenya Revenue Authority",
          status: "required",
          completionStatus: "pending"
        },
        {
          id: "3",
          name: "County Business Permit",
          description: "Apply for a single business permit from your county government",
          status: "required",
          completionStatus: "pending"
        },
        {
          id: "4",
          name: "NSSF Registration",
          description: hasEmployees ? "Required: Register with National Social Security Fund for employee benefits" : "Register with National Social Security Fund",
          status: hasEmployees ? "required" : "recommended",
          completionStatus: "pending"
        },
        {
          id: "5",
          name: "NHIF Registration",
          description: hasEmployees ? "Required: Register with National Hospital Insurance Fund for employees" : "Register with National Hospital Insurance Fund",
          status: hasEmployees ? "required" : "recommended",
          completionStatus: "pending"
        },
        {
          id: "6",
          name: "Fire Safety Certificate",
          description: "Obtain fire safety compliance certificate from county fire department",
          status: "optional",
          completionStatus: "pending"
        }
      ];
      
      setComplianceItems(mockData);
      setIsLoading(false);
      toast.success("Compliance check completed!");
    }, 1500);
  };

  const handleFileUpload = (itemId: string, event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const allowedTypes = ["application/pdf", "image/jpeg", "image/png"];
    if (!allowedTypes.includes(file.type)) {
      toast.error("Only PDF, JPG, and PNG files are allowed");
      return;
    }

    setComplianceItems(prev => prev.map(item => 
      item.id === itemId 
        ? {
            ...item,
            completionStatus: "done" as const,
            uploadedFile: {
              name: file.name,
              type: file.type,
              timestamp: Date.now()
            }
          }
        : item
    ));

    toast.success(`${file.name} uploaded successfully`);
  };

  const calculateProgress = () => {
    if (complianceItems.length === 0) return 0;
    const completed = complianceItems.filter(item => item.completionStatus === "done").length;
    return Math.round((completed / complianceItems.length) * 100);
  };

  const getMissingSuggestions = () => {
    const pending = complianceItems.filter(item => item.completionStatus === "pending");
    if (pending.length === 0) return ["🎉 All compliance items completed! You're fully compliant."];
    
    return pending.slice(0, 3).map(item => {
      if (item.name.includes("NHIF") && hasEmployees) {
        return `You haven't uploaded your NHIF certificate — required for businesses with employees.`;
      }
      if (item.name.includes("NSSF") && hasEmployees) {
        return `You haven't uploaded your NSSF certificate — required for businesses with employees.`;
      }
      return `${item.name} is ${item.status} but not yet uploaded.`;
    });
  };

  const downloadChecklist = () => {
    const element = document.getElementById("compliance-report");
    if (!element) return;

    const opt = {
      margin: 1,
      filename: `${businessName.replace(/\s+/g, "_")}_Compliance_Report_${new Date().toISOString().split("T")[0]}.pdf`,
      image: { type: "jpeg" as const, quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: "in", format: "letter", orientation: "portrait" as const }
    };

    html2pdf().set(opt).from(element).save();
    toast.success("Downloading compliance report...");
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "required":
        return "bg-destructive text-destructive-foreground";
      case "recommended":
        return "bg-secondary text-secondary-foreground";
      case "optional":
        return "bg-muted text-muted-foreground";
      default:
        return "bg-muted text-muted-foreground";
    }
  };

  const progressData = [
    { name: "Your Business", value: calculateProgress(), fill: "hsl(var(--primary))" },
    { name: "Sector Average", value: sectorBenchmark, fill: "hsl(var(--muted-foreground))" }
  ];

  return (
    <div className="space-y-8">
      <Card className="max-w-4xl mx-auto shadow-card">
        <CardHeader className="gradient-hero text-primary-foreground rounded-t-xl">
          <CardTitle className="text-2xl flex items-center gap-2">
            <CheckCircle2 className="h-6 w-6" />
            Compliance Checker
          </CardTitle>
          <CardDescription className="text-primary-foreground/80">
            Generate your personalized compliance checklist based on your business profile
          </CardDescription>
        </CardHeader>
        <CardContent className="p-6 space-y-6">
          {/* Business Profile Form */}
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="business-name" className="flex items-center gap-2">
                <Building2 className="h-4 w-4" />
                Business Name *
              </Label>
              <Input
                id="business-name"
                placeholder="Enter your business name"
                value={businessName}
                onChange={(e) => setBusinessName(e.target.value)}
              />
            </div>

            <div className="grid gap-4 md:grid-cols-3">
              <div className="space-y-2">
                <Label className="flex items-center gap-2">
                  <Briefcase className="h-4 w-4" />
                  Business Type *
                </Label>
                <Select value={businessType} onValueChange={setBusinessType}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="sole">Sole Proprietor</SelectItem>
                    <SelectItem value="partnership">Partnership</SelectItem>
                    <SelectItem value="limited">Limited Company</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label className="flex items-center gap-2">
                  <Briefcase className="h-4 w-4" />
                  Sector *
                </Label>
                <Select value={sector} onValueChange={setSector}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select sector" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="retail">Retail</SelectItem>
                    <SelectItem value="services">Services</SelectItem>
                    <SelectItem value="manufacturing">Manufacturing</SelectItem>
                    <SelectItem value="health">Health</SelectItem>
                    <SelectItem value="food">Food</SelectItem>
                    <SelectItem value="tech">Technology</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label className="flex items-center gap-2">
                  <MapPin className="h-4 w-4" />
                  Region / County *
                </Label>
                <Select value={region} onValueChange={setRegion}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select region" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="nairobi">Nairobi</SelectItem>
                    <SelectItem value="kiambu">Kiambu</SelectItem>
                    <SelectItem value="nakuru">Nakuru</SelectItem>
                    <SelectItem value="mombasa">Mombasa</SelectItem>
                    <SelectItem value="kisumu">Kisumu</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="space-y-0.5">
                  <Label htmlFor="has-employees" className="flex items-center gap-2">
                    <Users className="h-4 w-4" />
                    Has Employees
                  </Label>
                  <p className="text-xs text-muted-foreground">Do you have any employees?</p>
                </div>
                <Switch
                  id="has-employees"
                  checked={hasEmployees}
                  onCheckedChange={setHasEmployees}
                />
              </div>

              <div className="space-y-2">
                <Label className="flex items-center gap-2">
                  <UserCheck className="h-4 w-4" />
                  Owner Category
                </Label>
                <Select value={ownerCategory} onValueChange={setOwnerCategory}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select category" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="youth">Youth</SelectItem>
                    <SelectItem value="woman">Woman</SelectItem>
                    <SelectItem value="pwd">PWD</SelectItem>
                    <SelectItem value="none">None</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="space-y-0.5">
                  <Label htmlFor="ecitizen" className="text-sm font-medium">
                    eCitizen Account
                  </Label>
                  <p className="text-xs text-muted-foreground">Do you have an eCitizen account?</p>
                </div>
                <Switch
                  id="ecitizen"
                  checked={hasECitizen}
                  onCheckedChange={setHasECitizen}
                />
              </div>

              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="space-y-0.5">
                  <Label htmlFor="bank" className="text-sm font-medium">
                    Bank Account
                  </Label>
                  <p className="text-xs text-muted-foreground">Business or personal bank account?</p>
                </div>
                <Switch
                  id="bank"
                  checked={hasBankAccount}
                  onCheckedChange={setHasBankAccount}
                />
              </div>
            </div>
          </div>

          <Button 
            onClick={checkCompliance} 
            disabled={isLoading}
            className="w-full bg-primary hover:bg-primary/90"
          >
            {isLoading ? "Generating Checklist..." : "Generate Compliance Checklist"}
          </Button>

          {complianceItems.length > 0 && (
            <div id="compliance-report" className="space-y-6 pt-6">
              {/* Progress Summary */}
              <Card className="gradient-card">
                <CardHeader>
                  <CardTitle className="text-lg">Compliance Progress</CardTitle>
                  <CardDescription>Track your compliance journey</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-muted-foreground">Completion</span>
                      <span className="font-medium">{calculateProgress()}%</span>
                    </div>
                    <Progress value={calculateProgress()} className="h-3" />
                  </div>

                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={progressData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                        <XAxis dataKey="name" stroke="hsl(var(--muted-foreground))" />
                        <YAxis stroke="hsl(var(--muted-foreground))" />
                        <Tooltip 
                          contentStyle={{ 
                            backgroundColor: "hsl(var(--card))", 
                            border: "1px solid hsl(var(--border))",
                            borderRadius: "var(--radius)"
                          }}
                        />
                        <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                          {progressData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.fill} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </CardContent>
              </Card>

              {/* Checklist */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-foreground">
                    Compliance Checklist ({complianceItems.length} items)
                  </h3>
                  <Button 
                    variant="outline" 
                    size="sm" 
                    onClick={downloadChecklist}
                    className="flex items-center gap-2"
                  >
                    <Download className="h-4 w-4" />
                    Download PDF
                  </Button>
                </div>

                <div className="space-y-3">
                  {complianceItems.map((item) => (
                    <Card key={item.id} className="border-l-4" style={{
                      borderLeftColor: item.status === "required" ? "hsl(var(--destructive))" : item.status === "recommended" ? "hsl(var(--secondary))" : "hsl(var(--muted))"
                    }}>
                      <CardContent className="p-4">
                        <div className="space-y-3">
                          <div className="flex items-start gap-3">
                            {item.completionStatus === "done" ? (
                              <CheckCircle2 className="h-5 w-5 text-secondary mt-0.5" />
                            ) : (
                              <AlertCircle className="h-5 w-5 text-muted-foreground mt-0.5" />
                            )}
                            <div className="flex-1 space-y-2">
                              <div className="flex items-center gap-2 flex-wrap">
                                <h4 className="font-medium text-foreground">{item.name}</h4>
                                <Badge className={getStatusColor(item.status)} variant="secondary">
                                  {item.status}
                                </Badge>
                                {item.completionStatus === "done" && (
                                  <Badge variant="outline" className="bg-secondary/10 text-secondary border-secondary">
                                    ✓ Done
                                  </Badge>
                                )}
                              </div>
                              <p className="text-sm text-muted-foreground">{item.description}</p>

                              {item.uploadedFile ? (
                                <div className="flex items-center gap-2 p-2 bg-muted/50 rounded-md">
                                  <FileCheck className="h-4 w-4 text-secondary" />
                                  <span className="text-xs text-foreground">{item.uploadedFile.name}</span>
                                  <span className="text-xs text-muted-foreground">
                                    ({new Date(item.uploadedFile.timestamp).toLocaleDateString()})
                                  </span>
                                </div>
                              ) : (
                                <div>
                                  <Label 
                                    htmlFor={`upload-${item.id}`}
                                    className="inline-flex items-center gap-2 px-3 py-2 border rounded-md cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors"
                                  >
                                    <Upload className="h-4 w-4" />
                                    <span className="text-sm">Upload Document</span>
                                  </Label>
                                  <Input
                                    id={`upload-${item.id}`}
                                    type="file"
                                    accept=".pdf,.jpg,.jpeg,.png"
                                    className="hidden"
                                    onChange={(e) => handleFileUpload(item.id, e)}
                                  />
                                  <p className="text-xs text-muted-foreground mt-1">
                                    Accepts: PDF, JPG, PNG
                                  </p>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>

              {/* Suggestions Panel */}
              <Card className="bg-primary/5 border-primary/20">
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <AlertCircle className="h-5 w-5 text-primary" />
                    Recommendations
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {getMissingSuggestions().map((suggestion, index) => (
                      <li key={index} className="text-sm text-foreground flex items-start gap-2">
                        <span className="text-primary mt-0.5">•</span>
                        <span>{suggestion}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              {/* Branded Footer */}
              <div className="text-xs text-muted-foreground p-4 bg-muted/30 rounded-lg border">
                <p className="font-medium mb-1">📋 Report Summary</p>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <p><strong>Business:</strong> {businessName}</p>
                  <p><strong>Type:</strong> {businessType}</p>
                  <p><strong>Sector:</strong> {sector}</p>
                  <p><strong>Region:</strong> {region}</p>
                </div>
                <p className="mt-2 text-xs">
                  Generated on {new Date().toLocaleDateString()} • Powered by <strong>Inua360</strong>
                </p>
                <p className="mt-1 text-xs italic">
                  💡 This checklist is AI-generated. For precise requirements, consult with BRF or legal advisors.
                </p>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default ComplianceChecker;

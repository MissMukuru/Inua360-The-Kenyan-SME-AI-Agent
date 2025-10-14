import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Textarea } from "./ui/textarea";
import { Progress } from "./ui/progress";
import { 
  DollarSign, 
  TrendingUp, 
  PieChart as PieChartIcon, 
  Download, 
  Plus, 
  Trash2,
  Lightbulb,
  BadgeDollarSign,
  Info
} from "lucide-react";
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { useToast } from "@/hooks/use-toast";
import html2pdf from "html2pdf.js";

interface ExpenseCategory {
  id: string;
  category: string;
  amount: number;
}

interface FinancialData {
  businessName: string;
  businessSize: string;
  sector: string;
  monthlyIncome: number;
  expenses: ExpenseCategory[];
  financialGoals: string;
}

const FinanceCompanion = () => {
  const { toast } = useToast();
  const [formData, setFormData] = useState<FinancialData>({
    businessName: "",
    businessSize: "",
    sector: "",
    monthlyIncome: 0,
    expenses: [],
    financialGoals: ""
  });
  const [newExpense, setNewExpense] = useState({ category: "", amount: 0 });
  const [showResults, setShowResults] = useState(false);

  const sectors = ["Retail", "Services", "Manufacturing", "Health", "Food", "Technology", "Agriculture"];
  const businessSizes = ["Micro", "Small", "Medium"];

  const addExpense = () => {
    if (newExpense.category && newExpense.amount > 0) {
      setFormData({
        ...formData,
        expenses: [
          ...formData.expenses,
          { id: Date.now().toString(), ...newExpense }
        ]
      });
      setNewExpense({ category: "", amount: 0 });
      toast({
        title: "Expense added",
        description: `${newExpense.category} - KES ${newExpense.amount.toLocaleString()}`
      });
    }
  };

  const removeExpense = (id: string) => {
    setFormData({
      ...formData,
      expenses: formData.expenses.filter(exp => exp.id !== id)
    });
  };

  const calculateResults = () => {
    if (!formData.businessName || !formData.businessSize || !formData.sector || formData.monthlyIncome === 0) {
      toast({
        title: "Missing information",
        description: "Please fill in all required fields",
        variant: "destructive"
      });
      return;
    }
    setShowResults(true);
    toast({
      title: "Analysis complete",
      description: "Your financial summary is ready"
    });
  };

  const totalExpenses = formData.expenses.reduce((sum, exp) => sum + exp.amount, 0);
  const cashFlow = formData.monthlyIncome - totalExpenses;
  const savingsRate = formData.monthlyIncome > 0 ? ((cashFlow / formData.monthlyIncome) * 100) : 0;
  
  // Financial Health Score (0-100)
  const calculateHealthScore = () => {
    let score = 50; // Base score
    if (savingsRate > 20) score += 30;
    else if (savingsRate > 10) score += 20;
    else if (savingsRate > 0) score += 10;
    else score -= 20;
    
    if (formData.expenses.length >= 3) score += 10; // Good expense tracking
    if (formData.financialGoals) score += 10; // Has goals
    
    return Math.max(0, Math.min(100, score));
  };

  const healthScore = calculateHealthScore();

  // Mock data for charts
  const cashFlowData = [
    { name: "Income", value: formData.monthlyIncome, fill: "hsl(var(--primary))" },
    { name: "Expenses", value: totalExpenses, fill: "hsl(var(--destructive))" },
    { name: "Savings", value: Math.max(0, cashFlow), fill: "hsl(var(--chart-2))" }
  ];

  const expenseBreakdown = formData.expenses.map((exp, idx) => ({
    name: exp.category,
    value: exp.amount,
    fill: `hsl(var(--chart-${(idx % 5) + 1}))`
  }));

  // Mock recommendations
  const getRecommendations = () => {
    const tips = [];
    if (savingsRate < 10) {
      tips.push({
        title: "Improve Savings Rate",
        description: "Your savings rate is below 10%. Try to reduce expenses or increase income.",
        icon: "💰"
      });
    }
    if (formData.expenses.length < 3) {
      tips.push({
        title: "Track More Expenses",
        description: "Add more expense categories to get better insights into your spending.",
        icon: "📊"
      });
    }
    if (!formData.financialGoals) {
      tips.push({
        title: "Set Financial Goals",
        description: "Define clear financial goals to guide your business decisions.",
        icon: "🎯"
      });
    }
    if (cashFlow < 0) {
      tips.push({
        title: "Negative Cash Flow",
        description: "Your expenses exceed income. Review expenses or find ways to increase revenue.",
        icon: "⚠️"
      });
    } else {
      tips.push({
        title: "Positive Cash Flow",
        description: "Great! Consider investing surplus funds or building an emergency fund.",
        icon: "✅"
      });
    }
    return tips;
  };

  // Mock funding opportunities
  const fundingOpportunities = [
    {
      title: "WEDF Loan",
      type: "Micro-loan",
      amount: "Up to KES 50,000",
      description: "Low-interest loan for women entrepreneurs",
      eligibility: "Women-owned businesses, registered with KRA"
    },
    {
      title: "Uwezo Fund",
      type: "Grant",
      amount: "KES 10,000 - 500,000",
      description: "Youth and women empowerment fund",
      eligibility: "Youth, women, and PWD-owned businesses"
    },
    {
      title: "SME Credit Scheme",
      type: "Business Loan",
      amount: "Up to KES 500,000",
      description: "Affordable credit for small businesses",
      eligibility: "Registered businesses with bank accounts"
    },
    {
      title: "KCB Business Loan",
      type: "Loan",
      amount: "KES 50,000 - 5M",
      description: "Flexible repayment terms for SMEs",
      eligibility: "Active business bank account"
    }
  ];

  const downloadReport = () => {
    const element = document.getElementById("financial-report");
    const opt = {
      margin: 10,
      filename: `${formData.businessName}_Financial_Report.pdf`,
      image: { type: "jpeg" as const, quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: "mm", format: "a4", orientation: "portrait" as const }
    };

    html2pdf().set(opt).from(element).save();
    toast({
      title: "Report downloaded",
      description: "Your financial report has been saved"
    });
  };

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header */}
      <Card className="shadow-card">
        <CardHeader className="gradient-hero text-primary-foreground rounded-t-xl">
          <CardTitle className="text-2xl flex items-center gap-2">
            <DollarSign className="h-6 w-6" />
            Finance Companion
          </CardTitle>
          <CardDescription className="text-primary-foreground/80">
            Get personalized financial insights and funding recommendations
          </CardDescription>
        </CardHeader>
      </Card>

      {/* Input Form */}
      <Card className="shadow-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Business Financial Profile
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="businessName">Business Name *</Label>
              <Input
                id="businessName"
                placeholder="Enter business name"
                value={formData.businessName}
                onChange={(e) => setFormData({ ...formData, businessName: e.target.value })}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="businessSize">Business Size *</Label>
              <Select value={formData.businessSize} onValueChange={(value) => setFormData({ ...formData, businessSize: value })}>
                <SelectTrigger>
                  <SelectValue placeholder="Select size" />
                </SelectTrigger>
                <SelectContent>
                  {businessSizes.map(size => (
                    <SelectItem key={size} value={size}>{size}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="sector">Sector *</Label>
              <Select value={formData.sector} onValueChange={(value) => setFormData({ ...formData, sector: value })}>
                <SelectTrigger>
                  <SelectValue placeholder="Select sector" />
                </SelectTrigger>
                <SelectContent>
                  {sectors.map(sector => (
                    <SelectItem key={sector} value={sector}>{sector}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="monthlyIncome">Monthly Income (KES) *</Label>
              <Input
                id="monthlyIncome"
                type="number"
                placeholder="0"
                value={formData.monthlyIncome || ""}
                onChange={(e) => setFormData({ ...formData, monthlyIncome: parseFloat(e.target.value) || 0 })}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="financialGoals">Financial Goals (Optional)</Label>
            <Textarea
              id="financialGoals"
              placeholder="E.g., Expand to new location, hire 2 employees, buy equipment..."
              value={formData.financialGoals}
              onChange={(e) => setFormData({ ...formData, financialGoals: e.target.value })}
            />
          </div>

          {/* Expenses Section */}
          <div className="space-y-4">
            <Label className="text-base font-semibold">Monthly Expenses</Label>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Input
                placeholder="Category (e.g., Rent)"
                value={newExpense.category}
                onChange={(e) => setNewExpense({ ...newExpense, category: e.target.value })}
              />
              <Input
                type="number"
                placeholder="Amount (KES)"
                value={newExpense.amount || ""}
                onChange={(e) => setNewExpense({ ...newExpense, amount: parseFloat(e.target.value) || 0 })}
              />
              <Button onClick={addExpense} className="w-full">
                <Plus className="h-4 w-4 mr-2" />
                Add Expense
              </Button>
            </div>

            {formData.expenses.length > 0 && (
              <div className="space-y-2">
                {formData.expenses.map(expense => (
                  <div key={expense.id} className="flex items-center justify-between p-3 bg-muted rounded-lg">
                    <div>
                      <p className="font-medium">{expense.category}</p>
                      <p className="text-sm text-muted-foreground">KES {expense.amount.toLocaleString()}</p>
                    </div>
                    <Button variant="ghost" size="icon" onClick={() => removeExpense(expense.id)}>
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
                <div className="flex justify-between items-center pt-2 border-t">
                  <p className="font-semibold">Total Expenses</p>
                  <p className="font-semibold">KES {totalExpenses.toLocaleString()}</p>
                </div>
              </div>
            )}
          </div>

          <Button onClick={calculateResults} className="w-full" size="lg">
            Generate Financial Summary
          </Button>
        </CardContent>
      </Card>

      {/* Results Section */}
      {showResults && (
        <div className="space-y-8" id="financial-report">
          {/* Financial Health Score */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BadgeDollarSign className="h-5 w-5" />
                Financial Health Score
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="text-center">
                <div className="text-5xl font-bold text-primary mb-2">{healthScore}%</div>
                <Progress value={healthScore} className="h-3 mb-2" />
                <p className="text-sm text-muted-foreground flex items-center justify-center gap-2">
                  <Info className="h-4 w-4" />
                  Based on savings rate, expense tracking, and financial goals
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Cash Flow Summary */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Cash Flow Summary
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={cashFlowData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                    {cashFlowData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.fill} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
              <div className="mt-4 p-4 bg-muted rounded-lg">
                <div className="flex justify-between items-center">
                  <span className="font-medium">Net Cash Flow:</span>
                  <span className={`font-bold text-lg ${cashFlow >= 0 ? 'text-chart-2' : 'text-destructive'}`}>
                    KES {cashFlow.toLocaleString()}
                  </span>
                </div>
                <div className="flex justify-between items-center mt-2">
                  <span className="text-sm text-muted-foreground">Savings Rate:</span>
                  <span className="text-sm font-medium">{savingsRate.toFixed(1)}%</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Expense Breakdown */}
          {formData.expenses.length > 0 && (
            <Card className="shadow-card">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <PieChartIcon className="h-5 w-5" />
                  Expense Breakdown
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={expenseBreakdown}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      dataKey="value"
                    >
                      {expenseBreakdown.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.fill} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          )}

          {/* Recommendations */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Lightbulb className="h-5 w-5" />
                Personalized Recommendations
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {getRecommendations().map((tip, idx) => (
                <div key={idx} className="p-4 bg-muted rounded-lg">
                  <div className="flex items-start gap-3">
                    <span className="text-2xl">{tip.icon}</span>
                    <div>
                      <h4 className="font-semibold mb-1">{tip.title}</h4>
                      <p className="text-sm text-muted-foreground">{tip.description}</p>
                    </div>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Funding Opportunities */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <DollarSign className="h-5 w-5" />
                Funding Opportunities
              </CardTitle>
              <CardDescription>
                Based on your business profile and sector
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {fundingOpportunities.map((fund, idx) => (
                <div key={idx} className="p-4 border rounded-lg hover:bg-muted/50 transition-colors">
                  <div className="flex items-start justify-between mb-2">
                    <h4 className="font-semibold text-lg">{fund.title}</h4>
                    <span className="text-xs font-medium px-2 py-1 bg-primary/10 text-primary rounded">
                      {fund.type}
                    </span>
                  </div>
                  <p className="text-sm font-medium text-primary mb-2">{fund.amount}</p>
                  <p className="text-sm text-muted-foreground mb-2">{fund.description}</p>
                  <p className="text-xs text-muted-foreground">
                    <span className="font-medium">Eligibility:</span> {fund.eligibility}
                  </p>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Export Button */}
          <div className="flex justify-center">
            <Button onClick={downloadReport} size="lg" className="gap-2">
              <Download className="h-5 w-5" />
              Download Financial Report
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default FinanceCompanion;

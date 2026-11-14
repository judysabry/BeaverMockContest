import PDFKit
for p in CommandLine.arguments.dropFirst() {
  guard let d = PDFDocument(url: URL(fileURLWithPath: p)) else { print("FAIL", p); continue }
  for i in 0..<d.pageCount { if let t = d.page(at: i)?.string { print("=== \(p) page \(i+1)"); print(t) } }
}

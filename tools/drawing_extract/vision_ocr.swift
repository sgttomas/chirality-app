#!/usr/bin/env swift

import AppKit
import Foundation
import Vision

struct OCRLine: Codable {
    let text: String
    let confidence: Float
    let x: Double
    let y: Double
    let width: Double
    let height: Double
}

struct OCRResult: Codable {
    let image_path: String
    let image_width: Double
    let image_height: Double
    let lines: [OCRLine]
}

func fail(_ message: String) -> Never {
    FileHandle.standardError.write(Data((message + "\n").utf8))
    exit(2)
}

guard CommandLine.arguments.count >= 2 else {
    fail("Usage: vision_ocr.swift <image_path>")
}

let imagePath = CommandLine.arguments[1]
let imageURL = URL(fileURLWithPath: imagePath)

guard let image = NSImage(contentsOf: imageURL) else {
    fail("ERROR: could not open image: \(imagePath)")
}

var proposedRect = CGRect(origin: .zero, size: image.size)
guard let cgImage = image.cgImage(forProposedRect: &proposedRect, context: nil, hints: nil) else {
    fail("ERROR: could not decode image: \(imagePath)")
}

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = false
request.minimumTextHeight = 0.008

let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
do {
    try handler.perform([request])
} catch {
    fail("ERROR: Vision OCR failed: \(error)")
}

let observations = (request.results as? [VNRecognizedTextObservation]) ?? []
let lines: [OCRLine] = observations.compactMap { observation in
    guard let candidate = observation.topCandidates(1).first else {
        return nil
    }
    let box = observation.boundingBox
    return OCRLine(
        text: candidate.string,
        confidence: candidate.confidence,
        x: Double(box.minX),
        y: Double(box.minY),
        width: Double(box.width),
        height: Double(box.height)
    )
}

let sorted = lines.sorted {
    if abs($0.y - $1.y) > 0.002 {
        return $0.y > $1.y
    }
    return $0.x < $1.x
}

let result = OCRResult(
    image_path: imagePath,
    image_width: Double(cgImage.width),
    image_height: Double(cgImage.height),
    lines: sorted
)

let encoder = JSONEncoder()
encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
do {
    let data = try encoder.encode(result)
    FileHandle.standardOutput.write(data)
    FileHandle.standardOutput.write(Data("\n".utf8))
} catch {
    fail("ERROR: could not encode OCR JSON: \(error)")
}
